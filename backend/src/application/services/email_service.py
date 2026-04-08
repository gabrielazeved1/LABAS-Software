# backend/src/application/services/email_service.py
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO


class EmailService:
    @staticmethod
    def enviar_laudo_cliente(laudo, pdf_buffer: BytesIO) -> bool:
        """
        Envia o PDF do laudo em anexo para o e-mail do cliente.
        O PDF é lido estritamente a partir do buffer de memória (Memory-Safe).
        """
        cliente = laudo.cliente

        if not cliente.email:
            raise ValueError(
                f"O cliente {cliente.nome} não possui um e-mail registado."
            )

        assunto = f"Resultados da Análise de Solo - Laudo {laudo.id}"
        corpo = (
            f"Olá {cliente.nome},\n\n"
            f"O seu laudo técnico referente à emissão {laudo.data_emissao} "
            "já se encontra disponível.\n\n"
            "Segue em anexo o documento PDF com os resultados detalhados.\n\n"
            "Com os melhores cumprimentos,\n"
            "Equipa LABAS"
        )

        email = EmailMessage(
            subject=assunto,
            body=corpo,
            from_email=settings.DEFAULT_FROM_EMAIL,  # Requer configuração no settings.py
            to=[cliente.email],
        )

        # Reposicionar o ponteiro do buffer para o início antes de ler
        pdf_buffer.seek(0)

        # Anexar o ficheiro a partir da RAM
        email.attach(
            filename=f"Laudo_{laudo.id}_LABAS.pdf",
            content=pdf_buffer.read(),
            mimetype="application/pdf",
        )

        try:
            email.send(fail_silently=False)
            return True
        except Exception as e:
            # Ponto de extensão futuro para integração com um sistema de logs (ex: Sentry)
            print(f"Erro no EmailService: {str(e)}")
            return False
