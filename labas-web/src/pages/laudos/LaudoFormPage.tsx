import { useState } from "react";
import { Controller } from "react-hook-form";
import {
  Autocomplete,
  Box,
  Button,
  Grid,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import PageHeader from "../../components/shared/PageHeader";
import LoadingOverlay from "../../components/shared/LoadingOverlay";
import { useLaudoForm } from "../../hooks/useLaudoForm";
import { useClientes } from "../../hooks/useClientes";
import type { Cliente } from "../../types/cliente";

export default function LaudoFormPage() {
  const { form, submitting, onSubmit } = useLaudoForm();
  const { clientes, loading, buscar, limpar } = useClientes();
  const [clienteSelecionado, setClienteSelecionado] = useState<Cliente | null>(
    null,
  );
  const [clienteInput, setClienteInput] = useState("");

  const handleClienteInput = (_: React.SyntheticEvent, value: string) => {
    setClienteInput(value);
    if (value.trim().length === 0) {
      if (clienteSelecionado) {
        setClienteSelecionado(null);
        form.setValue("cliente_codigo", "", {
          shouldDirty: true,
          shouldValidate: true,
        });
      }
      limpar();
      return;
    }
    if (value.trim().length < 2) {
      limpar();
      return;
    }
    buscar(value);
  };

  return (
    <Box component="form" onSubmit={onSubmit} noValidate>
      <LoadingOverlay open={submitting} message="Salvando laudo..." />

      <PageHeader
        title="Novo Laudo"
        subtitle="Informe o cliente e a data de entrada. As análises são adicionadas depois."
      />

      <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
        <Typography variant="subtitle1" fontWeight={700} mb={2}>
          Dados do laudo
        </Typography>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 8 }}>
            <Controller
              control={form.control}
              name="cliente_codigo"
              render={({ field, fieldState }) => (
                <Autocomplete
                  options={clientes}
                  value={clienteSelecionado}
                  inputValue={clienteInput}
                  onInputChange={handleClienteInput}
                  onChange={(_, value) => {
                    setClienteSelecionado(value);
                    field.onChange(value?.codigo ?? "");
                  }}
                  onBlur={field.onBlur}
                  loading={loading}
                  noOptionsText={
                    clienteInput.length < 2
                      ? "Digite pelo menos 2 caracteres"
                      : "Nenhum cliente encontrado"
                  }
                  getOptionLabel={(option) =>
                    `${option.codigo} — ${option.nome}`
                  }
                  isOptionEqualToValue={(option, value) =>
                    option.codigo === value.codigo
                  }
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Cliente *"
                      size="small"
                      error={!!fieldState.error}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />
              )}
            />
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <TextField
              fullWidth
              size="small"
              label="Data de Entrada *"
              type="date"
              slotProps={{ inputLabel: { shrink: true } }}
              error={!!form.formState.errors.data_emissao}
              helperText={form.formState.errors.data_emissao?.message}
              disabled={submitting}
              {...form.register("data_emissao")}
            />
          </Grid>

          {clienteSelecionado && (
            <Grid size={12}>
              <Typography variant="body2" color="text.secondary">
                {clienteSelecionado.municipio} • {clienteSelecionado.area}
              </Typography>
            </Grid>
          )}

          <Grid size={12}>
            <TextField
              fullWidth
              size="small"
              label="Observações"
              multiline
              rows={3}
              disabled={submitting}
              {...form.register("observacoes")}
            />
          </Grid>
        </Grid>
      </Paper>

      <Stack direction={{ xs: "column", sm: "row" }} spacing={2} mb={4}>
        <Button variant="outlined" component={RouterLink} to="/laudos">
          Voltar
        </Button>
        <Button type="submit" variant="contained" disabled={submitting}>
          {submitting ? "Salvando..." : "Criar laudo"}
        </Button>
      </Stack>
    </Box>
  );
}
