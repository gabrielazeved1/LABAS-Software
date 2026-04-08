import { useState } from "react";
import { Button, CircularProgress, Stack, Tooltip } from "@mui/material";
import EmailIcon from "@mui/icons-material/Email";
import WhatsAppIcon from "@mui/icons-material/WhatsApp";
import { laudoService } from "../../services/laudoService";
import { gerarLinkWhatsApp } from "../../utils/whatsapp";
import { useSnackbar } from "../../hooks/useSnackbar";

interface BotoesComunicacaoProps {
  laudoId: number;
  clienteNome: string;
  clienteTelefone?: string;
}

export function BotoesComunicacao({
  laudoId,
  clienteNome,
  clienteTelefone,
}: BotoesComunicacaoProps) {
  const [isEmailLoading, setIsEmailLoading] = useState(false);
  const { showSuccess, showError, showWarning } = useSnackbar();

  const handleWhatsApp = () => {
    if (!clienteTelefone) {
      showWarning("O cliente não possui um telefone registado.");
      return;
    }
    const link = gerarLinkWhatsApp(
      clienteTelefone,
      String(laudoId),
      clienteNome,
    );
    window.open(link, "_blank", "noopener,noreferrer");
  };

  const handleEmail = async () => {
    setIsEmailLoading(true);
    try {
      await laudoService.enviarPorEmail(laudoId);
      showSuccess("E-mail enviado com sucesso para o cliente!");
    } catch (error) {
      showError(
        "Erro ao enviar o e-mail. Verifique se o cliente possui um e-mail válido.",
      );
    } finally {
      setIsEmailLoading(false);
    }
  };

  return (
    <Stack direction="row" spacing={1}>
      <Tooltip title="Enviar notificação por WhatsApp">
        <Button
          variant="outlined"
          color="success"
          size="small"
          startIcon={<WhatsAppIcon />}
          onClick={handleWhatsApp}
          sx={{ textTransform: "none" }}
        >
          WhatsApp
        </Button>
      </Tooltip>

      <Tooltip title="Enviar Laudo em anexo (PDF) por E-mail">
        <Button
          variant="contained"
          color="primary"
          size="small"
          startIcon={
            isEmailLoading ? (
              <CircularProgress size={20} color="inherit" />
            ) : (
              <EmailIcon />
            )
          }
          onClick={handleEmail}
          disabled={isEmailLoading}
          sx={{ textTransform: "none" }}
        >
          {isEmailLoading ? "A Enviar..." : "E-mail"}
        </Button>
      </Tooltip>
    </Stack>
  );
}
