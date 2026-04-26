"""
Gerador de legendas em português a partir de vídeos com áudio em inglês.

Este script utiliza:
- tkinter: para interface gráfica de seleção de arquivos
- moviepy: para extrair áudio do vídeo
- speech_recognition: para transcrever áudio (inglês)
- deep_translator: para traduzir o texto para português brasileiro

Fluxo:
1. Extrai o áudio do vídeo
2. Transcreve o áudio em inglês (Google Speech Recognition)
3. Se online falhar, usa Vosk offline como fallback
4. Traduz o texto para português brasileiro
5. Gera arquivo SRT com a legenda

Uso: python aula065.py caminho_do_video.mp4
       python aula065.py --selecionar  (abre caixa de seleção de arquivos)
"""

import os
import sys
import subprocess
from pathlib import Path


def selecionar_arquivo():
    """Abre uma caixa de diálogo para selecionar um arquivo de vídeo."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        print("❌ Tkinter não está disponível. Instale-o para usar a interface gráfica.")
        return None

    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    file_path = filedialog.askopenfilename(
        title="Selecione um vídeo para processar",
        filetypes=[
            ("Arquivos de vídeo", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
            ("Todos os arquivos", "*.*"),
        ],
    )

    root.destroy()

    if file_path:
        print(f"📹 Vídeo selecionado: {file_path}")
        return file_path
    return None


def verificar_dependencias():
    """Verifica e instala dependências se necessário."""
    dependencias_ok = True

    try:
        import speech_recognition as sr
    except ImportError:
        print("⚠️  Instalando dependência: SpeechRecognition")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "SpeechRecognition"])
            import speech_recognition as sr
        except subprocess.CalledProcessError:
            print("❌ Falha ao instalar SpeechRecognition. Execute:")
            print("   pip install SpeechRecognition --break-system-packages")
            print("   ou use um ambiente virtual: python3 -m venv venv && source venv/bin/activate && pip install SpeechRecognition")
            dependencias_ok = False

    try:
        from moviepy import VideoFileClip
    except ImportError:
        print("⚠️  Instalando dependência: moviepy")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
            from moviepy import VideoFileClip
        except subprocess.CalledProcessError:
            print("❌ Falha ao instalar moviepy. Execute:")
            print("   pip install moviepy --break-system-packages")
            dependencias_ok = False

    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("⚠️  Instalando dependência: deep_translator")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "deep_translator"])
            from deep_translator import GoogleTranslator
        except subprocess.CalledProcessError:
            print("❌ Falha ao instalar deep_translator. Execute:")
            print("   pip install deep_translator --break-system-packages")
            dependencias_ok = False

    return dependencias_ok


def extrair_audio(video_path, audio_path):
    """Extrai o áudio de um arquivo de vídeo e salva em formato WAV."""
    from moviepy import VideoFileClip

    print(f"📹 Extraindo áudio do vídeo: {video_path}")

    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec='pcm_s16le')
        audio.close()
        video.close()
        print(f"✅ Áudio extraído com sucesso: {audio_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao extrair áudio: {e}")
        return False


def transcrever_audio_offline_vosk(audio_path, idioma='pt'):
    """Transcreve áudio offline usando Vosk."""
    try:
        from vosk import Model, KaldiRecognizer
        import json
    except ImportError:
        print("❌ Vosk não está instalado. Execute: pip install vosk --break-system-packages")
        return None

    print("🎤 Transcrevendo offline com Vosk...")
    print("⏳ Carregando modelo (isso pode demorar na primeira vez)...")

    try:
        import urllib.request
        import zipfile

        # Modelos disponíveis
        modelos = {
            'pt': {
                'url': 'https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip',
                'nome': 'vosk-model-small-pt-0.3',
                'descricao': 'português'
            },
            'en': {
                'url': 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip',
                'nome': 'vosk-model-small-en-us-0.15',
                'descricao': 'inglês'
            }
        }

        modelo_info = modelos.get(idioma, modelos['pt'])
        model_path = Path.home() / ".vosk-models" / modelo_info['nome']

        # Baixar modelo se não existir
        if not model_path.exists():
            model_path.parent.mkdir(parents=True, exist_ok=True)
            zip_path = model_path.parent / "model.zip"

            print(f"⬇️  Baixando modelo de {modelo_info['descricao']} (~50MB)...")
            urllib.request.urlretrieve(modelo_info['url'], zip_path)

            print("📦 Extraindo modelo...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(model_path.parent)
            zip_path.unlink()

        # Carregar modelo
        model = Model(str(model_path))

        # Processar áudio
        import wave
        wf = wave.open(audio_path, 'rb')
        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)

        print("⏳ Transcrevendo...")
        texto_completo = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                resultado = json.loads(recognizer.Result())
                if 'text' in resultado and resultado['text']:
                    texto_completo.append(resultado['text'])

        # Resultado final
        resultado_final = json.loads(recognizer.FinalResult())
        if 'text' in resultado_final and resultado_final['text']:
            texto_completo.append(resultado_final['text'])

        wf.close()

        texto = ' '.join(texto_completo).strip()
        if texto:
            print(f"✅ Transcrição offline concluída!")
            return texto
        else:
            print("⚠️  Transcrição vazia")
            return None

    except Exception as e:
        print(f"❌ Erro na transcrição offline: {e}")
        return None


def transcrever_audio(audio_path, tentativas=2):
    """Transcreve áudio em inglês usando Google Speech Recognition com fallback offline."""
    import speech_recognition as sr
    import time

    print(f"🎤 Transcrevendo áudio (inglês -> português)...")

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000
    recognizer.dynamic_energy_threshold = False

    # Tentar transcrição online (inglês)
    for tentativa in range(1, tentativas + 1):
        try:
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)

            print(f"⏳ Transcrevendo em inglês... (tentativa {tentativa}/{tentativas})")
            
            texto = recognizer.recognize_google(
                audio_data,
                language='en-US'
            )
            print(f"✅ Transcrição concluída")
            return texto

        except sr.RequestError as e:
            erro_msg = str(e)
            print(f"⚠️  Tentativa {tentativa}: Erro de conexão: {erro_msg}")
            
            if tentativa < tentativas:
                espera = 3 if "Broken pipe" in erro_msg else 5
                print(f"⏳ Aguardando {espera} segundos...")
                time.sleep(espera)
            else:
                print(f"❌ Falha na transcrição online após {tentativas} tentativas.")

        except sr.UnknownValueError:
            print(f"⚠️  Tentativa {tentativa}: Áudio não reconhecido")
            if tentativa < tentativas:
                time.sleep(3)
            else:
                print(f"❌ Falha na transcrição online após {tentativas} tentativas.")

        except Exception as e:
            print(f"❌ Tentativa {tentativa}: Erro inesperado: {e}")
            if tentativa < tentativas:
                time.sleep(5)
            else:
                print(f"❌ Falha na transcrição online após {tentativas} tentativas.")

    # Fallback offline com Vosk (inglês)
    print("\n🔄 Tentando transcrição offline com Vosk (modelo em inglês)...")
    texto_offline = transcrever_audio_offline_vosk(audio_path, idioma='en')
    
    if texto_offline:
        return texto_offline
    
    print("\n❌ Todas as opções de transcrição falharam.")
    print("💡 Verifique sua conexão ou instale vosk: pip install vosk --break-system-packages")
    return None


def dividir_em_segmentos(texto, max_palavras=15):
    """Divide o texto transcrito em segmentos para legendas."""
    palavras = texto.split()
    segmentos = []

    for i in range(0, len(palavras), max_palavras):
        segmento = ' '.join(palavras[i:i + max_palavras])
        segmentos.append(segmento)

    return segmentos


def traduzir_texto(texto, idioma_origem='en', idioma_destino='pt'):
    """Traduz um texto de um idioma de origem para um idioma de destino."""
    from deep_translator import GoogleTranslator

    print(f"🌐 Traduzindo texto de {idioma_origem} para {idioma_destino}")

    try:
        tradutor = GoogleTranslator(source=idioma_origem, target=idioma_destino)
        texto_traduzido = tradutor.translate(texto)
        print(f"✅ Tradução concluída")
        return texto_traduzido
    except Exception as e:
        print(f"❌ Erro na tradução: {e}")
        return None


def formatar_tempo(segundos):
    """Formata segundos no formato SRT (00:00:00,000)."""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = int(segundos % 60)
    milissegundos = int((segundos % 1) * 1000)

    return f"{horas:02d}:{minutos:02d}:{segs:02d},{milissegundos:03d}"


def gerar_legenda_srt_simples(segmentos_traduzidos, duracao_video, output_path):
    """Gera um arquivo de legenda SRT com o texto traduzido e timestamps distribuídos."""
    print(f"📝 Gerando arquivo de legenda (português): {output_path}")

    try:
        num_segmentos = len(segmentos_traduzidos)
        duracao_segmento = duracao_video / num_segmentos

        with open(output_path, 'w', encoding='utf-8') as f:
            for i, texto_legenda in enumerate(segmentos_traduzidos, 1):
                inicio = (i - 1) * duracao_segmento
                fim = i * duracao_segmento

                f.write(f"{i}\n")
                f.write(f"{formatar_tempo(inicio)} --> {formatar_tempo(fim)}\n")
                f.write(f"{texto_legenda}\n")
                f.write("\n")

        print(f"✅ Legenda em português gerada: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar legenda: {e}")
        return False


def processar_video(video_path, idioma_origem='en', idioma_destino='pt'):
    """Processa o vídeo: extrai áudio, transcreve (inglês), traduz e gera legenda em português."""
    from moviepy import VideoFileClip

    video_path = Path(video_path)

    if not video_path.exists():
        print(f"❌ Arquivo de vídeo não encontrado: {video_path}")
        return False

    print("=" * 60)
    print("🎬 INICIANDO PROCESSAMENTO DE VÍDEO 🎬")
    print("=" * 60)

    # Paths para arquivos temporários e de saída
    diretorio = video_path.parent
    nome_video = video_path.stem
    audio_path = diretorio / f"{nome_video}_audio.wav"
    srt_saida = diretorio / f"{nome_video}_legendas_pt.srt"

    try:
        # Passo 1: Extrair áudio
        if not extrair_audio(str(video_path), str(audio_path)):
            return False

        # Passo 2: Obter duração do vídeo
        video = VideoFileClip(str(video_path))
        duracao_video = video.duration
        video.close()

        # Passo 3: Transcrever áudio (inglês)
        texto_transcrito = transcrever_audio(str(audio_path))
        if not texto_transcrito:
            return False

        print(f"\n📄 Texto transcrito (inglês):\n{texto_transcrito}\n")

        # Passo 4: Dividir em segmentos para legendas
        segmentos_ingles = dividir_em_segmentos(texto_transcrito)
        print(f"📋 Texto dividido em {len(segmentos_ingles)} segmentos")

        # Passo 5: Traduzir cada segmento para português
        segmentos_portugues = []
        print("⏳ Traduzindo segmentos para português...")
        for i, segmento in enumerate(segmentos_ingles, 1):
            print(f"  Traduzindo segmento {i}/{len(segmentos_ingles)}")
            traduzido = traduzir_texto(segmento, idioma_origem, idioma_destino)
            if traduzido:
                segmentos_portugues.append(traduzido)
            else:
                segmentos_portugues.append(segmento)

        # Passo 6: Gerar legenda apenas em português
        if not gerar_legenda_srt_simples(
            segmentos_portugues, duracao_video, str(srt_saida)
        ):
            return False

        print("\n" + "=" * 60)
        print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print(f"📁 Legenda gerada: {srt_saida}")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ Erro durante o processamento: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Limpar arquivo de áudio temporário
        if audio_path.exists():
            print(f"\n🗑️  Limpando arquivo temporário: {audio_path}")
            audio_path.unlink()


if __name__ == "__main__":
    # Verifica se deve abrir a caixa de seleção de arquivos
    if "--selecionar" in sys.argv or "-s" in sys.argv:
        print("🎬 Gerador de Legendas em Português (áudio em inglês)")
        print("=" * 60)
        print("\n📂 Abrindo caixa de seleção de arquivos...")

        # Primeiro abre a caixa de seleção (antes de verificar dependências)
        video_file = selecionar_arquivo()

        if not video_file:
            print("❌ Nenhum arquivo selecionado. Encerrando.")
            sys.exit(1)

        # Agora verifica as dependências
        if not verificar_dependencias():
            print("\n⚠️  Nem todas as dependências foram instaladas.")
            print("Instale-as manualmente e tente novamente:")
            print("   pip install SpeechRecognition moviepy deep_translator --break-system-packages")
            sys.exit(1)

        sucesso = processar_video(video_file)
        sys.exit(0 if sucesso else 1)

    elif len(sys.argv) < 2:
        print("🎬 Gerador de Legendas em Português (áudio em inglês)")
        print("=" * 60)
        print("\n📖 Uso: python aula065.py <caminho_do_video>")
        print("     python aula065.py --selecionar  (abre caixa de seleção de arquivos)")
        print("\n💡 Exemplo:")
        print("   python aula065.py video.mp4")
        print("   python aula065.py --selecionar")
        print("\n📋 Funcionamento:")
        print("   1. Extrai o áudio do vídeo")
        print("   2. Transcreve o áudio em inglês")
        print("   3. Traduz para português brasileiro")
        print("   4. Gera arquivo .srt com a legenda")
        print("\n📦 Arquivo gerado:")
        print("   - {video}_legendas_pt.srt")
        sys.exit(1)

    else:
        # Modo linha de comando com caminho direto
        if not verificar_dependencias():
            print("\n⚠️  Nem todas as dependências foram instaladas.")
            print("Instale-as manualmente e tente novamente:")
            print("   pip install SpeechRecognition moviepy deep_translator --break-system-packages")
            sys.exit(1)

        video_file = sys.argv[1]
        sucesso = processar_video(video_file)
        sys.exit(0 if sucesso else 1)
