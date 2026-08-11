import { useMemo } from "react";
import {
  Alert,
  Autocomplete,
  Box,
  Button,
  Chip,
  CircularProgress,
  FormControl,
  InputLabel,
  LinearProgress,
  MenuItem,
  Select,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import {
  DataGrid,
  type GridColDef,
  type GridRenderCellParams,
} from "@mui/x-data-grid";
import SaveOutlinedIcon from "@mui/icons-material/SaveOutlined";
import PageHeader from "../../components/shared/PageHeader";
import { useEntradaLote } from "../../hooks/useEntradaLote";
import {
  EQUIPAMENTOS,
  ELEMENTOS_POR_EQUIPAMENTO,
  ELEMENTO_LABEL,
  LEITURA_LABEL,
  REQUER_VOLUMES,
  SEM_CURVA_CALIBRACAO,
} from "../../config/calibracaoConstants";
import type { Equipamento, Elemento } from "../../types/calibracao";
import type { Laudo } from "../../types/analise";
import type { LinhaBancada } from "../../types/entradaLote";

const STATUS_CHIP: Record<
  LinhaBancada["status"],
  { label: string; color: "default" | "success" | "error" }
> = {
  pendente: { label: "Pendente", color: "default" },
  salvo: { label: "Salvo", color: "success" },
  erro: { label: "Erro", color: "error" },
};

export default function EntradaLotePage() {
  const {
    laudoInput,
    laudoSelecionado,
    laudoOpcoes,
    loadingLaudos,
    handleLaudoInput,
    handleLaudoChange,
    equipamento,
    handleSetEquipamento,
    elemento,
    handleSetElemento,
    baterias,
    loadingBaterias,
    bateriaSelecionada,
    setBateriaSelecionada,
    jaFiltrou,
    linhas,
    loadingAmostras,
    salvando,
    handleFiltrar,
    handleProcessRowUpdate,
  } = useEntradaLote();

  const elementosDisponiveis = equipamento
    ? ELEMENTOS_POR_EQUIPAMENTO[equipamento as Equipamento]
    : [];

  const leituraLabel = equipamento
    ? LEITURA_LABEL[equipamento as Equipamento]
    : "Leitura";

  const exibirFator = equipamento
    ? REQUER_VOLUMES.includes(equipamento as Equipamento)
    : false;

  const columns = useMemo<GridColDef<LinhaBancada>[]>(() => [
    {
      field: "n_lab",
      headerName: "N. Lab",
      width: 130,
      sortable: false,
    },
    {
      field: "cliente_nome",
      headerName: "Cliente",
      flex: 1,
      minWidth: 160,
      sortable: false,
    },
    ...(exibirFator
      ? [
          {
            field: "fator_diluicao",
            headerName: "Fator Diluição",
            width: 150,
            sortable: false,
            editable: true,
          } as GridColDef<LinhaBancada>,
        ]
      : []),
    {
      field: "leitura_bruta",
      headerName: leituraLabel,
      width: 180,
      sortable: false,
      editable: true,
    },
    {
      field: "resultado_preview",
      headerName: "Resultado Calculado",
      width: 180,
      sortable: false,
      renderCell: (params: GridRenderCellParams<LinhaBancada>) => {
        const val = params.row.resultado_preview;
        return (
          <Typography
            variant="body2"
            color={val !== null ? "primary" : "text.disabled"}
          >
            {val !== null ? val.toFixed(4) : "—"}
          </Typography>
        );
      },
    },
    {
      field: "status",
      headerName: "Status",
      width: 110,
      sortable: false,
      renderCell: (params: GridRenderCellParams<LinhaBancada>) => {
        const { label, color } = STATUS_CHIP[params.row.status];
        return <Chip label={label} color={color} size="small" />;
      },
    },
    {
      field: "acoes",
      headerName: "",
      width: 60,
      sortable: false,
      renderCell: (params: GridRenderCellParams<LinhaBancada>) => {
        const row = params.row;
        const loading = salvando[row.n_lab] ?? false;
        if (loading) {
          return <CircularProgress size={16} />;
        }
        return (
          <Tooltip title="Edite a célula para salvar">
            <span>
              <Button
                size="small"
                variant="text"
                disabled
                aria-label={`Aguardando edição de ${row.n_lab}`}
              >
                <SaveOutlinedIcon fontSize="small" />
              </Button>
            </span>
          </Tooltip>
        );
      },
    },
  ], [exibirFator, leituraLabel, salvando]);

  const renderPainelCurva = () => {
    if (!jaFiltrou || !bateriaSelecionada) return null;
    if (SEM_CURVA_CALIBRACAO.includes(bateriaSelecionada.equipamento)) return null;
    if (loadingAmostras) return null;

    if (
      bateriaSelecionada.coeficiente_angular_a === null ||
      bateriaSelecionada.coeficiente_linear_b === null
    ) {
      return (
        <Alert severity="warning" sx={{ mb: 2 }}>
          Bateria selecionada ainda não tem curva calculada. Adicione pelo menos
          2 pontos em <strong>Calibração</strong>.
        </Alert>
      );
    }

    return (
      <Alert severity="info" sx={{ mb: 2 }}>
        <div>
          <strong>Curva:</strong> {bateriaSelecionada.equacao_formada}
          {bateriaSelecionada.r_quadrado !== null && (
            <span style={{ marginLeft: 16 }}>
              R² = {Number(bateriaSelecionada.r_quadrado).toFixed(6)}
            </span>
          )}
        </div>
        <div style={{ marginTop: 6 }}>
          <strong>Branco:</strong> {bateriaSelecionada.leitura_branco ?? "—"} |{" "}
          <strong>V-solo:</strong> {bateriaSelecionada.volume_solo ?? "—"} |{" "}
          <strong>V-extrator:</strong> {bateriaSelecionada.volume_extrator ?? "—"}
        </div>
      </Alert>
    );
  };

  return (
    <Box>
      <PageHeader
        title="Amostras"
        subtitle="Bancada de digitação de leituras brutas por elemento"
      />

      {/* Filtros */}
      <Stack
        direction={{ xs: "column", sm: "row" }}
        spacing={2}
        mb={3}
        alignItems="flex-end"
        flexWrap="wrap"
      >
        <Autocomplete<Laudo>
          options={laudoOpcoes}
          value={laudoSelecionado}
          inputValue={laudoInput}
          onInputChange={handleLaudoInput}
          onChange={handleLaudoChange}
          loading={loadingLaudos}
          noOptionsText={
            laudoInput.length < 2
              ? "Digite pelo menos 2 caracteres"
              : "Nenhum laudo encontrado"
          }
          getOptionLabel={(option) => option.codigo_laudo}
          isOptionEqualToValue={(option, value) => option.id === value.id}
          sx={{ minWidth: 200 }}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Laudo (opcional)"
              size="small"
              slotProps={{
                input: {
                  ...params.InputProps,
                  endAdornment: (
                    <>
                      {loadingLaudos && <CircularProgress size={16} />}
                      {params.InputProps.endAdornment}
                    </>
                  ),
                },
              }}
            />
          )}
        />

        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel id="eq-label">Equipamento</InputLabel>
          <Select
            labelId="eq-label"
            label="Equipamento"
            value={equipamento}
            onChange={(e) => handleSetEquipamento(e.target.value as Equipamento)}
          >
            {EQUIPAMENTOS.map((eq) => (
              <MenuItem key={eq.value} value={eq.value}>
                {eq.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl size="small" sx={{ minWidth: 200 }} disabled={!equipamento}>
          <InputLabel id="el-label">Elemento</InputLabel>
          <Select
            labelId="el-label"
            label="Elemento"
            value={elemento}
            onChange={(e) => handleSetElemento(e.target.value as Elemento)}
          >
            {elementosDisponiveis.map((el) => (
              <MenuItem key={el} value={el}>
                {ELEMENTO_LABEL[el]}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl
          size="small"
          sx={{ minWidth: 260 }}
          disabled={!elemento || loadingBaterias}
        >
          <InputLabel id="bat-label">
            {loadingBaterias ? "Carregando baterias…" : "Bateria / Calibração"}
          </InputLabel>
          <Select
            labelId="bat-label"
            label={loadingBaterias ? "Carregando baterias…" : "Bateria / Calibração"}
            value={bateriaSelecionada?.id ?? ""}
            onChange={(e) => {
              const bat = baterias.find((b) => b.id === Number(e.target.value));
              setBateriaSelecionada(bat ?? null);
            }}
          >
            {baterias.length === 0 && !loadingBaterias && (
              <MenuItem disabled value="">
                Nenhuma bateria cadastrada
              </MenuItem>
            )}
            {baterias.map((bat) => (
              <MenuItem key={bat.id} value={bat.id}>
                {new Date(bat.data_criacao).toLocaleDateString("pt-BR", {
                  day: "2-digit",
                  month: "2-digit",
                  year: "numeric",
                })}
                {bat.leitura_branco !== null && ` — Branco: ${bat.leitura_branco}`}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button
          variant="contained"
          disabled={!bateriaSelecionada || loadingAmostras}
          onClick={handleFiltrar}
        >
          Carregar
        </Button>
      </Stack>

      {renderPainelCurva()}

      {(loadingAmostras || linhas.length > 0) && (
        <Box sx={{ width: "100%" }}>
          {loadingAmostras && <LinearProgress sx={{ mb: 1 }} />}
          <DataGrid
            rows={linhas}
            columns={columns}
            getRowId={(row) => row.n_lab}
            processRowUpdate={handleProcessRowUpdate}
            onProcessRowUpdateError={(error) => console.error(error)}
            autoHeight
            disableColumnMenu
            disableRowSelectionOnClick
            hideFooterSelectedRowCount
            pageSizeOptions={[25, 50, 100]}
            initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
            getRowClassName={(params) =>
              params.row.status === "salvo" ? "row-salvo" : ""
            }
            sx={{
              "& .row-salvo": { opacity: 0.5 },
              "& .MuiDataGrid-cell": { alignItems: "center", display: "flex" },
            }}
          />
        </Box>
      )}

      {!loadingAmostras &&
        jaFiltrou &&
        bateriaSelecionada &&
        linhas.length === 0 && (
          <Alert severity="success">
            {laudoSelecionado ? (
              <>
                Todas as amostras do laudo{" "}
                <strong>{laudoSelecionado.codigo_laudo}</strong> para{" "}
                <strong>{ELEMENTO_LABEL[elemento as Elemento]}</strong> já foram
                processadas nesta bateria.
              </>
            ) : (
              <>
                Todas as amostras para{" "}
                <strong>{ELEMENTO_LABEL[elemento as Elemento]}</strong> já foram
                processadas nesta bateria.
              </>
            )}
          </Alert>
        )}
    </Box>
  );
}
