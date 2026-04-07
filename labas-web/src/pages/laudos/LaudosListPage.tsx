import { useMemo, useState } from "react";
import {
  Box,
  TextField,
  IconButton,
  Typography,
  Paper,
  CircularProgress,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import type { GridColDef } from "@mui/x-data-grid";
import VisibilityIcon from "@mui/icons-material/Visibility";
import DeleteIcon from "@mui/icons-material/Delete";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import { useNavigate } from "react-router-dom";

import { useLaudos } from "../../hooks/useLaudos";

// ...existing code...
export default function LaudosListPage() {
  const navigate = useNavigate();

  const { data, loading, error, deleteLaudo, downloadPdf } = useLaudos();

  const [search, setSearch] = useState("");

  // 🔍 filtro local (pode evoluir para backend)
  const filteredData = useMemo(() => {
    return data.filter((l) =>
      l.n_lab.toLowerCase().includes(search.toLowerCase())
    );
  }, [data, search]);

  // 📊 definição das colunas
  const columns: GridColDef[] = [
    {
      field: "n_lab",
      headerName: "N Lab",
      flex: 1,
    },
    {
      field: "cliente_nome",
      headerName: "Cliente",
      flex: 1.5,
    },
    {
      field: "data_entrada",
      headerName: "Entrada",
      flex: 1,
    },
    {
      field: "data_saida",
      headerName: "Saída",
      flex: 1,
      valueGetter: (params: { value: string | null }) => params.value || "-",
    },
    {
      field: "actions",
      headerName: "Ações",
      flex: 1,
      sortable: false,
      renderCell: (params) => {
        const nLab = params.row.n_lab;

        return (
          <>
            {/* 👁 ver detalhe */}
            <IconButton
              onClick={() => navigate(`/laudos/${nLab}`)}
            >
              <VisibilityIcon />
            </IconButton>

            {/* 📄 PDF */}
            <IconButton
              onClick={() => downloadPdf(nLab)}
            >
              <PictureAsPdfIcon />
            </IconButton>

            {/* ❌ deletar */}
            <IconButton
              onClick={() => deleteLaudo(nLab)}
            >
              <DeleteIcon />
            </IconButton>
          </>
        );
      },
    },
  ];

  // 🧱 estado de loading
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box p={2}>
      <Typography variant="h5" mb={2}>
        Laudos
      </Typography>

      {/* ⚠️ erro */}
      {error && (
        <Typography color="error" mb={2}>
          {error}
        </Typography>
      )}

      {/* 🔍 busca */}
      <TextField
        label="Buscar por N Lab"
        fullWidth
        size="small"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        sx={{ mb: 2 }}
      />

      {/* 📊 tabela */}
      <Paper>
        <DataGrid
          rows={filteredData}
          columns={columns}
          getRowId={(row) => row.n_lab} // chave única
          pageSizeOptions={[10]}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 10, page: 0 },
            },
          }}
          disableRowSelectionOnClick
          autoHeight
        />
      </Paper>
    </Box>
  );
}