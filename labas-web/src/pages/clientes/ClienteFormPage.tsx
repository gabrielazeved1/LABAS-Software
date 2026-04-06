import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Controller } from "react-hook-form";
import {
  Box,
  Button,
  CircularProgress,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useClienteForm } from "../../hooks/useClienteForm";
import { clienteService } from "../../services/clienteService";
import { useSnackbar } from "../../hooks/useSnackbar";
import type { Cliente } from "../../types/cliente";

export default function ClienteFormPage() {
  const { codigo } = useParams<{ codigo?: string }>();
  const navigate = useNavigate();
  const { showApiError } = useSnackbar();
  const edicao = !!codigo;

  const [clienteInicial, setClienteInicial] = useState<Cliente | undefined>();
  const [buscando, setBuscando] = useState(edicao);

  useEffect(() => {
    if (!edicao || !codigo) return;
    clienteService
      .buscar(codigo)
      .then(setClienteInicial)
      .catch(showApiError)
      .finally(() => setBuscando(false));
  }, [codigo, edicao, showApiError]);

  const { form, loading, onSubmit } = useClienteForm({
    clienteInicial,
    onSucesso: () => navigate("/clientes"),
  });

  const {
    control,
    formState: { errors },
  } = form;

  if (buscando) {
    return (
      <Box display="flex" justifyContent="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} color="primary" gutterBottom>
        {edicao ? "Editar Cliente" : "Novo Cliente"}
      </Typography>

      <Paper variant="outlined" sx={{ p: 3, maxWidth: 600 }}>
        <Stack component="form" onSubmit={onSubmit} spacing={2}>
          <Controller
            name="codigo"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Código"
                error={!!errors.codigo}
                helperText={errors.codigo?.message}
                disabled={edicao}
                required
              />
            )}
          />
          <Controller
            name="nome"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Nome / Razão Social"
                error={!!errors.nome}
                helperText={errors.nome?.message}
                required
              />
            )}
          />
          <Controller
            name="municipio"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Município"
                error={!!errors.municipio}
                helperText={errors.municipio?.message}
              />
            )}
          />
          <Controller
            name="area"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Área"
                error={!!errors.area}
                helperText={errors.area?.message}
              />
            )}
          />
          <Controller
            name="contato"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Contato"
                error={!!errors.contato}
                helperText={errors.contato?.message}
              />
            )}
          />
          <Controller
            name="observacoes"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Observações"
                multiline
                rows={3}
                error={!!errors.observacoes}
                helperText={errors.observacoes?.message}
              />
            )}
          />

          <Stack direction="row" spacing={1} justifyContent="flex-end">
            <Button variant="outlined" onClick={() => navigate("/clientes")}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained" disabled={loading}>
              {loading ? (
                <CircularProgress size={20} />
              ) : edicao ? (
                "Salvar"
              ) : (
                "Criar"
              )}
            </Button>
          </Stack>
        </Stack>
      </Paper>
    </Box>
  );
}
