// src/components/shared/EmptyState.tsx
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import InboxIcon from "@mui/icons-material/Inbox";
import type { ReactNode } from "react";

interface Props {
  /** Título principal da mensagem de estado vazio */
  title?: string;
  /** Descrição secundária */
  description?: string;
  /** Ação opcional (ex: botão "Criar novo laudo") */
  action?: ReactNode;
}

/**
 * Estado vazio padronizado para tabelas e listas sem resultados.
 *
 * Use sempre que uma listagem retornar `results: []` da API.
 * Aceita uma `action` opcional para guiar o usuário ao próximo passo.
 */
export default function EmptyState({
  title = "Nenhum item encontrado",
  description,
  action,
}: Props) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      gap={2}
      py={8}
      color="text.secondary"
    >
      <InboxIcon sx={{ fontSize: 56, opacity: 0.4 }} />
      <Typography variant="h6" color="text.secondary" textAlign="center">
        {title}
      </Typography>
      {description && (
        <Typography variant="body2" color="text.secondary" textAlign="center">
          {description}
        </Typography>
      )}
      {action}
    </Box>
  );
}
