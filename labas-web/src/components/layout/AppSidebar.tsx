// src/components/layout/AppSidebar.tsx
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import DashboardIcon from "@mui/icons-material/Dashboard";
import ScienceIcon from "@mui/icons-material/Science";
import AssignmentIcon from "@mui/icons-material/Assignment";
import PeopleIcon from "@mui/icons-material/People";
import BiotechIcon from "@mui/icons-material/Biotech";
import MenuBookIcon from "@mui/icons-material/MenuBook";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

interface Props {
  width: number;
}

/** Itens de navegação visíveis para todos os usuários autenticados */
const navComum = [
  { label: "Dashboard", icon: <DashboardIcon />, to: "/dashboard" },
  { label: "Meus Laudos", icon: <AssignmentIcon />, to: "/laudos" },
  { label: "Guia de Uso", icon: <MenuBookIcon />, to: "/guia" },
];

/** Itens de navegação exclusivos de staff */
const navStaff = [
  { label: "Amostras", icon: <BiotechIcon />, to: "/entrada-lote" },
  { label: "Calibração", icon: <ScienceIcon />, to: "/calibracao" },
  { label: "Clientes", icon: <PeopleIcon />, to: "/clientes" },
];

/**
 * Sidebar lateral fixa do LABAS.
 *
 * Responsabilidades:
 * - Exibir a logo/nome do sistema.
 * - Renderizar os links de navegação comuns.
 * - Renderizar os links exclusivos de staff quando `isStaff = true`.
 * - Destacar o link ativo via NavLink.
 */
export default function AppSidebar({ width }: Props) {
  const { isStaff } = useAuth();

  const renderItems = (items: typeof navComum) =>
    items.map(({ label, icon, to }) => (
      <ListItem key={to} disablePadding>
        <ListItemButton
          component={NavLink}
          to={to}
          sx={{
            borderRadius: 1,
            mx: 1,
            "&.active": {
              bgcolor: "primary.main",
              color: "primary.contrastText",
              "& .MuiListItemIcon-root": { color: "primary.contrastText" },
            },
          }}
        >
          <ListItemIcon sx={{ minWidth: 36 }}>{icon}</ListItemIcon>
          <ListItemText primary={label} />
        </ListItemButton>
      </ListItem>
    ));

  return (
    <Drawer
      variant="permanent"
      sx={{
        width,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width,
          boxSizing: "border-box",
          borderRight: "1px solid",
          borderColor: "divider",
        },
      }}
    >
      {/* Logo / nome do sistema */}
      <Box sx={{ px: 2, py: 2.5 }}>
        <Typography variant="h6" color="primary" fontWeight={700}>
          LABAS
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Análise de Solos
        </Typography>
      </Box>

      <Divider />

      <List dense sx={{ mt: 1 }}>
        {renderItems(navComum)}

        {isStaff && (
          <>
            <Divider sx={{ my: 1 }} />
            {renderItems(navStaff)}
          </>
        )}
      </List>
    </Drawer>
  );
}
