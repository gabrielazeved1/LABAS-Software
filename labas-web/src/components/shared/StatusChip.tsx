// src/components/shared/StatusChip.tsx
import Chip, { type ChipProps } from "@mui/material/Chip";

type Status = "pendente" | "em_andamento" | "concluido" | "cancelado";

interface Props {
  status: Status;
  size?: ChipProps["size"];
}

const config: Record<Status, { label: string; color: ChipProps["color"] }> = {
  pendente: { label: "Pendente", color: "warning" },
  em_andamento: { label: "Em andamento", color: "info" },
  concluido: { label: "Concluído", color: "success" },
  cancelado: { label: "Cancelado", color: "error" },
};

/**
 * Chip padronizado para exibir o status de um laudo.
 *
 * Sempre use este componente ao exibir status — nunca crie chips ad-hoc nos
 * componentes de lista ou detalhe. Isso garante que cor e label sejam
 * consistentes em toda a aplicação.
 */
export default function StatusChip({ status, size = "small" }: Props) {
  const { label, color } = config[status];
  return <Chip label={label} color={color} size={size} variant="filled" />;
}
