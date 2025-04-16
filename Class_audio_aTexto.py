import whisper
#model = whisper.load_model("small")
# importante *self* se usa como *this* en otros lenguajes

class Audio_aTexto:
    def __init__(self, modelo="small"):
        self.model = whisper.load_model(modelo)

    def audio_aText_convert(self, audio_file_path):
        # Cargar un archivo de audio y extraer 30 seg
        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)

        # Crear espectrograma
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        # Detectar idioma
        _, probs = self.model.detect_language(mel)
        idioma = max(probs, key=probs.get)
        print(f"Idioma detectado: {idioma}")

        # Decodificar audio
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)

        # Imprimir el texto reconocido
        print(result.text)
        return {"idioma": idioma, "transcripcion": result.text}

    def audio_a_text(self,audio_file_path):
        # Cargar un archivo de audio y extraer 30 seg
        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)

        # Crear espectrograma
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        # Detectar idioma
        _, probs = self.model.detect_language(mel)
        idioma = max(probs, key=probs.get)
        print(f"Idioma detectado: {idioma}")

        # Decodificar audio
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)

        # Imprimir el texto reconocido
        print(result.text)
        return {"idioma": idioma, "transcripcion": result.text}