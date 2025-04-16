import gradio as gr
import whisper
model = whisper.load_model("medium")


def audio_toText(audio_file):
    # cargar un archivo de audio y extraer 30 seg
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    #crear espectrogrma
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    #detectar idioma
    _,probs = model.detect_language(mel)
    print(f"Idioma detectado:{max(probs,key=probs.get)}")

    #decodificar audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model,mel,options)

    #Imprimir el texto reconocido
    print(result.text)
    return result.text

#generar interface web
web = gr.Interface(
    fn=audio_toText,
    inputs=gr.Audio(
        sources=["microphone"],
        type="filepath",
        label="Español"
    ),
    outputs=[gr.Text()],
    title="TEXTO A VOZ",
    description="Modelo simple de prueba de traduccion de texto a voz"
)

web.launch()

