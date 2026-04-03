// src/components/layout/AppHeader.tsx
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import LogoutIcon from "@mui/icons-material/Logout";
import { useAuth } from "../../hooks/useAuth";

interface Props {
  /** Largura da sidebar para deslocar o header corretamente */
  sidebarWidth: number;
}

/**
 * Barra superior fixa do LABAS.
 *
 * Responsabilidades:
 * - Exibir o nome do usuário autenticado.
 * - Oferecer o botão de logout.
 * - Deslocar-se para a direita da sidebar via `ml` (margin-left).
 */
export default function AppHeader({ sidebarWidth }: Props) {
  const { user, logout } = useAuth();

  return (
    <AppBar
      position="fixed"
      elevation={0}
      color="inherit"
      sx={{
        width: { sm: `calc(100% - ${sidebarWidth}px)` },
        ml: { sm: `${sidebarWidth}px` },
        bgcolor: "background.paper",
        borderBottom: "1px solid",
        borderColor: "divider",
      }}
    >
      <Toolbar sx={{ justifyContent: "space-between" }}>
        <Typography variant="body1" fontWeight={600} color="text.primary">
          Olá, {user?.username ?? "—"}
        </Typography>

        <Tooltip title="Sair">
          <IconButton color="primary" onClick={logout} aria-label="sair">
            <LogoutIcon />
          </IconButton>
        </Tooltip>
      </Toolbar>
    </AppBar>
  );
}
