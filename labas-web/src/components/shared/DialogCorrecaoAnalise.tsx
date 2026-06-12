import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  Stack,
  Tab,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";
import { useCorrecaoAnalise } from "../../hooks/useCorrecaoAnalise";
import type { LeituraDetalhe } from "../../types/analise";

interface Props {
  open: boolean;
  laudoId: number;
  analiseId: number;
  onClose: () => void;
}

// ─── Aba 0: Correção de Bancada ───────────────────────────────────────────────

interface TabBancadaProps {
  leituras: LeituraDetalhe[];
  salvando: boolean;
  onCorrigir: (
    leituraId: number,
    leitura_bruta: number,
    fator_diluicao: number | null,
  ) => void;
}

function TabBancada({ leituras, salvando, onCorrigir }: TabBancadaProps) {
  // Estado local: mapa de leituraId -> { leitura_bruta, fator_diluicao }
  const [valores, setValores] = useState<
    Record<number, { leitura_bruta: string; fator_diluicao: string }>
  >(() =>
    Object.fromEntries(
      leituras.map((l) => [
        l.id,
        {
          leitura_bruta: String(l.leitura_bruta),
          fator_diluicao:
            l.fator_diluicao != null ? String(l.fator_diluicao) : "",
        },
      ]),
    ),
  );

  if (leituras.length === 0) {
    return (
      <Alert severity="info" sx={{ mt: 2 }}>
        Nenhuma leitura de bancada registrada para esta amostra.
      </Alert>
    );
  }

  return (
    <Stack spacing={3} mt={2}>
      <Alert severity="info">
        Ao salvar uma leitura corrigida, o backend recalcula automaticamente os
        índices <strong>SB, CTC, V% e m%</strong> via signal.
      </Alert>

      {leituras.map((l) => {
        const v = valores[l.id] ?? {
          leitura_bruta: String(l.leitura_bruta),
          fator_diluicao: "",
        };
        const leituraNum = parseFloat(v.leitura_bruta);
        const fatorNum =
          v.fator_diluicao !== "" ? parseFloat(v.fator_diluicao) : null;
        const invalido = isNaN(leituraNum);

        return (
          <Box key={l.id}>
            <Stack
              direction="row"
              alignItems="center"
              justifyContent="space-between"
              mb={1}
            >
              <Typography variant="subtitle2" fontWeight={700}>
                {l.elemento_display}{" "}
                <Typography
                  component="span"
                  variant="body2"
                  color="text.secondary"
                >
                  ({l.equipamento})
                </Typography>
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Resultado atual:{" "}
                <strong>
                  {l.resultado_calculado != null
                    ? l.resultado_calculado.toFixed(3)
                    : "—"}
                </strong>
              </Typography>
            </Stack>

            <Grid container spacing={1} alignItems="flex-end">
              <Grid size={{ xs: 12, sm: 5 }}>
                <TextField
                  label="Leitura bruta corrigida *"
                  size="small"
                  fullWidth
                  type="number"
                  value={v.leitura_bruta}
                  onChange={(e) =>
                    setValores((prev) => ({
                      ...prev,
                      [l.id]: { ...prev[l.id], leitura_bruta: e.target.value },
                    }))
                  }
                  error={invalido}
                  helperText={invalido ? "Valor inválido" : undefined}
                  inputProps={{ step: "any" }}
                />
              </Grid>

              {/* Fator de diluição apenas para AA, FC, ES */}
              {["AA", "FC", "ES"].includes(l.equipamento) && (
                <Grid size={{ xs: 12, sm: 4 }}>
                  <TextField
                    label="Fator de diluição *"
                    size="small"
                    fullWidth
                    type="number"
                    value={v.fator_diluicao}
                    onChange={(e) =>
                      setValores((prev) => ({
                        ...prev,
                        [l.id]: {
                          ...prev[l.id],
                          fator_diluicao: e.target.value,
                        },
                      }))
                    }
                    inputProps={{ step: "any", min: 1 }}
                  />
                </Grid>
              )}

              <Grid size={{ xs: 12, sm: 3 }}>
                <Button
                  variant="outlined"
                  size="small"
                  fullWidth
                  disabled={salvando || invalido}
                  onClick={() => onCorrigir(l.id, leituraNum, fatorNum)}
                >
                  Salvar
                </Button>
              </Grid>
            </Grid>
            <Divider sx={{ mt: 2 }} />
          </Box>
        );
      })}
    </Stack>
  );
}

// ─── Aba 1: Granulometria ─────────────────────────────────────────────────────

interface TabGranulometriaProps {
  areia: number | null;
  argila: number | null;
  silte: number | null;
  salvando: boolean;
  onSalvar: (v: {
    areia: number | null;
    argila: number | null;
    silte: number | null;
  }) => void;
}

function TabGranulometria({
  areia,
  argila,
  silte,
  salvando,
  onSalvar,
}: TabGranulometriaProps) {
  const [v, setV] = useState({
    areia: areia != null ? String(areia) : "",
    argila: argila != null ? String(argila) : "",
    silte: silte != null ? String(silte) : "",
  });

  const toNum = (s: string) => (s === "" ? null : parseFloat(s));
  const soma =
    (toNum(v.areia) ?? 0) + (toNum(v.argila) ?? 0) + (toNum(v.silte) ?? 0);
  const somaInvalida = soma > 100.01;

  return (
    <Stack spacing={2} mt={2}>
      {somaInvalida && (
        <Alert severity="warning">
          Soma de areia + argila + silte não pode ultrapassar 100%. Atual:{" "}
          <strong>{soma.toFixed(1)}%</strong>
        </Alert>
      )}

      <Grid container spacing={2}>
        {(
          [
            { key: "areia", label: "Areia (%)" },
            { key: "argila", label: "Argila (%)" },
            { key: "silte", label: "Silte (%)" },
          ] as const
        ).map(({ key, label }) => (
          <Grid key={key} size={{ xs: 12, sm: 4 }}>
            <TextField
              label={label}
              size="small"
              fullWidth
              type="number"
              value={v[key]}
              onChange={(e) =>
                setV((prev) => ({ ...prev, [key]: e.target.value }))
              }
              inputProps={{ step: "any", min: 0, max: 100 }}
            />
          </Grid>
        ))}
      </Grid>

      <Box>
        <Button
          variant="contained"
          disabled={salvando || somaInvalida}
          onClick={() =>
            onSalvar({
              areia: toNum(v.areia),
              argila: toNum(v.argila),
              silte: toNum(v.silte),
            })
          }
        >
          {salvando ? "Salvando..." : "Salvar Granulometria"}
        </Button>
      </Box>
    </Stack>
  );
}

// ─── Dialog principal ─────────────────────────────────────────────────────────

export default function DialogCorrecaoAnalise({
  open,
  laudoId,
  analiseId,
  onClose,
}: Props) {
  const [aba, setAba] = useState(0);
  const {
    analise,
    leituras,
    loading,
    salvando,
    corrigirLeitura,
    salvarGranulometria,
  } = useCorrecaoAnalise(
    open ? laudoId : undefined,
    open ? analiseId : undefined,
  );

  const handleCorrigir = async (
    leituraId: number,
    leitura_bruta: number,
    fator_diluicao: number | null,
  ) => {
    await corrigirLeitura(leituraId, {
      leitura_bruta,
      ...(fator_diluicao != null ? { fator_diluicao } : {}),
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      scroll="paper"
    >
      <DialogTitle>
        <Typography variant="h6" component="span">
          Correção da Amostra
        </Typography>
        {analise && (
          <Typography
            variant="h5"
            component="div"
            fontWeight={800}
            color="primary"
          >
            {analise.n_lab}
          </Typography>
        )}
      </DialogTitle>

      <Tabs
        value={aba}
        onChange={(_, v: number) => setAba(v)}
        sx={{ px: 3, borderBottom: 1, borderColor: "divider" }}
      >
        <Tab label="Correção de Bancada" />
        <Tab label="Granulometria" />
      </Tabs>

      <DialogContent>
        {loading ? (
          <Box display="flex" justifyContent="center" py={4}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            {aba === 0 && (
              <TabBancada
                leituras={leituras}
                salvando={salvando}
                onCorrigir={handleCorrigir}
              />
            )}
            {aba === 1 && analise && (
              <TabGranulometria
                areia={analise.areia}
                argila={analise.argila}
                silte={analise.silte}
                salvando={salvando}
                onSalvar={salvarGranulometria}
              />
            )}
          </>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Fechar</Button>
      </DialogActions>
    </Dialog>
  );
}
