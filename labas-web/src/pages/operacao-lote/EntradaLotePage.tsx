import {
  Alert,
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
import type { LinhaBancada } from "../../types/entradaLote";

// ─── helpers ────────────────────────────────────────────────────────────────

const STATUS_CHIP: Record<
  LinhaBancada["status"],
  { label: string; color: "default" | "success" | "error" }
> = {
  pendente: { label: "Pendente", color: "default" },
  salvo: { label: "Salvo", color: "success" },
  erro: { label: "Erro", color: "error" },
};

// ─── componente ─────────────────────────────────────────────────────────────

export default function EntradaLotePage() {
  const {
    equipamento,
    setEquipamento,
    elemento,
    setElemento,
    bateriaAtiva,
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

  // ─── colunas do DataGrid ──────────────────────────────────────────────────

  const columns: GridColDef<LinhaBancada>[] = [
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
  ];

  // ─── painel da curva ──────────────────────────────────────────────────────

  const renderPainelCurva = () => {
    // Só exibe após o primeiro "Carregar"
    if (!jaFiltrou) return null;

    // Ainda não filtrou
    if (!equipamento || !elemento) return null;

    // Equipamentos sem curva nao exibem painel de calibracao
    if (SEM_CURVA_CALIBRACAO.includes(equipamento as Equipamento)) return null;

    // Carregando
    if (loadingAmostras) return null;

    // Curva ativa de outro elemento/equipamento (defensivo)
    if (
      bateriaAtiva &&
      (bateriaAtiva.equipamento !== equipamento ||
        bateriaAtiva.elemento !== elemento)
    ) {
      return (
        <Alert severity="error" sx={{ mb: 2 }}>
          A curva ativa nao corresponde ao elemento selecionado. Ative a bateria
          correta em <strong>Calibracao</strong>.
        </Alert>
      );
    }

    // Sem bateria ativa
    if (!bateriaAtiva) {
      const equipamentoLabel =
        EQUIPAMENTOS.find((e) => e.value === equipamento)?.label ??
        "equipamento";
      return (
        <Alert severity="error" sx={{ mb: 2 }}>
          {equipamento === "AA" ? (
            <>Nao ha reta ativa na absorcao atomica.</>
          ) : (
            <>
              Nenhuma bateria ativa para{" "}
              <strong>{ELEMENTO_LABEL[elemento as Elemento]}</strong> no{" "}
              <strong>{equipamentoLabel}</strong>.
            </>
          )}{" "}
          Acesse <strong>Calibracao</strong> para ativar uma bateria.
        </Alert>
      );
    }

    // Bateria ativa sem curva calculada
    if (
      bateriaAtiva.coeficiente_angular_a === null ||
      bateriaAtiva.coeficiente_linear_b === null
    ) {
      return (
        <Alert severity="warning" sx={{ mb: 2 }}>
          {equipamento === "AA" ? (
            <>Nao ha reta ativa na absorcao atomica.</>
          ) : (
            <>
              Bateria ativa encontrada, mas a curva de calibracao ainda nao esta
              calculada.
            </>
          )}{" "}
          Adicione pelo menos 2 pontos em <strong>Calibracao</strong>.
        </Alert>
      );
    }

    // Bateria com curva OK
    return (
      <Alert severity="info" sx={{ mb: 2 }}>
        <div>
          <strong>Curva ativa:</strong> {bateriaAtiva.equacao_formada}
          {bateriaAtiva.r_quadrado !== null && (
            <span style={{ marginLeft: 16 }}>
              R² = {Number(bateriaAtiva.r_quadrado).toFixed(6)}
            </span>
          )}
        </div>
        <div style={{ marginTop: 6 }}>
          <strong>Branco:</strong> {bateriaAtiva.leitura_branco ?? "—"} |{" "}
          <strong>V-solo:</strong> {bateriaAtiva.volume_solo ?? "—"} |{" "}
          <strong>V-extrator:</strong> {bateriaAtiva.volume_extrator ?? "—"}
        </div>
      </Alert>
    );
  };

  // ─── render ───────────────────────────────────────────────────────────────

  return (
    <Box>
      <PageHeader
        title="Operação em Lote"
        subtitle="Bancada de digitação de leituras brutas por elemento"
      />

      {/* Filtros */}
      <Stack
        direction={{ xs: "column", sm: "row" }}
        spacing={2}
        mb={3}
        alignItems="flex-end"
      >
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel id="eq-label">Equipamento</InputLabel>
          <Select
            labelId="eq-label"
            label="Equipamento"
            value={equipamento}
            onChange={(e) => {
              setEquipamento(e.target.value as Equipamento);
              setElemento("");
            }}
          >
            {EQUIPAMENTOS.map((eq) => (
              <MenuItem key={eq.value} value={eq.value}>
                {eq.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl
          size="small"
          sx={{ minWidth: 200 }}
          disabled={!equipamento}
        >
          <InputLabel id="el-label">Elemento</InputLabel>
          <Select
            labelId="el-label"
            label="Elemento"
            value={elemento}
            onChange={(e) => setElemento(e.target.value as Elemento)}
          >
            {elementosDisponiveis.map((el) => (
              <MenuItem key={el} value={el}>
                {ELEMENTO_LABEL[el]}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button
          variant="contained"
          disabled={!equipamento || !elemento || loadingAmostras}
          onClick={handleFiltrar}
        >
          Carregar
        </Button>
      </Stack>

      {/* Painel da curva ativa */}
      {renderPainelCurva()}

      {/* Tabela */}
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

      {/* Estado vazio: filtrou mas não há amostras pendentes */}
      {!loadingAmostras &&
        equipamento &&
        elemento &&
        linhas.length === 0 &&
        bateriaAtiva !== null && (
          <Alert severity="success">
            Todas as amostras para{" "}
            <strong>{ELEMENTO_LABEL[elemento as Elemento]}</strong> já foram
            processadas nesta bateria.
          </Alert>
        )}
    </Box>
  );
}
