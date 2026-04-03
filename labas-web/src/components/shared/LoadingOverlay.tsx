// src/components/shared/LoadingOverlay.tsx
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";

interface Props {
  /** Controla a visibilidade do overlay */
  open: boolean;
  /** Mensagem opcional exibida abaixo do spinner */
  message?: string;
}

/**
 * Overlay de carregamento global com backdrop semitransparente.
 *
 * Use quando uma operação bloqueia toda a tela (ex: submit de formulário,
 * carregamento inicial de página). Para loading inline em tabelas ou cards,
 * prefira o CircularProgress diretamente no componente.
 */
export default function LoadingOverlay({
  open,
  message = "Carregando...",
}: Props) {
  return (
    <Backdrop
      open={open}
      sx={{ zIndex: (t) => t.zIndex.modal + 1, color: "#fff" }}
    >
      <Stack alignItems="center" gap={2}>
        <CircularProgress color="inherit" />
        <Typography variant="body2">{message}</Typography>
      </Stack>
    </Backdrop>
  );
}
