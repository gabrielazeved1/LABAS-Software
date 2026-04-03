// src/components/shared/ConfirmDialog.tsx
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";

interface Props {
  /** Controla a visibilidade do dialog */
  open: boolean;
  /** Título da confirmação */
  title?: string;
  /** Mensagem de confirmação */
  message: string;
  /** Label do botão de confirmação (destrutivo) */
  confirmLabel?: string;
  /** Label do botão de cancelamento */
  cancelLabel?: string;
  /** Callback ao confirmar */
  onConfirm: () => void;
  /** Callback ao cancelar ou fechar */
  onCancel: () => void;
  /** Indica que a operação está em andamento (desabilita botões) */
  loading?: boolean;
}

/**
 * Dialog de confirmação para ações destrutivas ou irreversíveis.
 *
 * Use para confirmar exclusões, cancelamentos ou qualquer ação que o usuário
 * não possa desfazer. Nunca use `window.confirm()`.
 *
 * @example
 * <ConfirmDialog
 *   open={dialogOpen}
 *   message="Deseja excluir este laudo permanentemente?"
 *   onConfirm={handleDelete}
 *   onCancel={() => setDialogOpen(false)}
 * />
 */
export default function ConfirmDialog({
  open,
  title = "Confirmar ação",
  message,
  confirmLabel = "Confirmar",
  cancelLabel = "Cancelar",
  onConfirm,
  onCancel,
  loading = false,
}: Props) {
  return (
    <Dialog open={open} onClose={onCancel} maxWidth="xs" fullWidth>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{message}</DialogContentText>
      </DialogContent>
      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button onClick={onCancel} disabled={loading} color="inherit">
          {cancelLabel}
        </Button>
        <Button
          onClick={onConfirm}
          disabled={loading}
          variant="contained"
          color="error"
          autoFocus
        >
          {confirmLabel}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
