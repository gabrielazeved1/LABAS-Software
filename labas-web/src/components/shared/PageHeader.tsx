// src/components/shared/PageHeader.tsx
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import type { ReactNode } from "react";

interface Props {
  /** Título da página */
  title: string;
  /** Subtítulo ou descrição opcional */
  subtitle?: string;
  /** Ações à direita do título (ex: botão "Novo Laudo") */
  actions?: ReactNode;
}

/**
 * Cabeçalho padronizado de página para todas as rotas internas.
 *
 * Mantém espaçamento e hierarquia tipográfica consistentes.
 * Sempre use este componente como primeiro filho do conteúdo de uma página —
 * nunca declare título/subtítulo inline em cada página.
 */
export default function PageHeader({ title, subtitle, actions }: Props) {
  return (
    <Box mb={3}>
      <Box
        display="flex"
        alignItems="center"
        justifyContent="space-between"
        mb={1}
      >
        <Box>
          <Typography variant="h5" fontWeight={700} color="text.primary">
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="body2" color="text.secondary" mt={0.5}>
              {subtitle}
            </Typography>
          )}
        </Box>
        {actions && <Box>{actions}</Box>}
      </Box>
      <Divider />
    </Box>
  );
}
