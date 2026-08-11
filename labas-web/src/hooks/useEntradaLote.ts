import { useState, useCallback, useRef } from "react";
import {
  calibracaoService,
  type BateriaCalibracaoComPontos,
} from "../services/calibracaoService";
import { entradaLoteService } from "../services/entradaLoteService";
import { laudoService } from "../services/laudoService";
import { useSnackbar } from "./useSnackbar";
import { REQUER_VOLUMES, SEM_CURVA_CALIBRACAO } from "../config/calibracaoConstants";
import type { Equipamento, Elemento } from "../types/calibracao";
import type { Laudo } from "../types/analise";
import type { LinhaBancada } from "../types/entradaLote";

const normalizeDecimalInput = (value: string) =>
  value.replace(/,/g, ".").trim();

export function useEntradaLote() {
  const { showSuccess, showError, showApiError } = useSnackbar();

  // ── Laudo ──────────────────────────────────────────────────────────────────
  const [laudoInput, setLaudoInput] = useState("");
  const [laudoSelecionado, setLaudoSelecionado] = useState<Laudo | null>(null);
  const [laudoOpcoes, setLaudoOpcoes] = useState<Laudo[]>([]);
  const [loadingLaudos, setLoadingLaudos] = useState(false);
  const laudoTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const laudoAbort = useRef<AbortController | null>(null);

  // ── Equipamento / Elemento ─────────────────────────────────────────────────
  const [equipamento, setEquipamento] = useState<Equipamento | "">("");
  const [elemento, setElemento] = useState<Elemento | "">("");

  // ── Bateria ────────────────────────────────────────────────────────────────
  const [baterias, setBaterias] = useState<BateriaCalibracaoComPontos[]>([]);
  const [loadingBaterias, setLoadingBaterias] = useState(false);
  const [bateriaSelecionada, setBateriaSelecionada] =
    useState<BateriaCalibracaoComPontos | null>(null);

  // ── Bancada ────────────────────────────────────────────────────────────────
  const [linhas, setLinhas] = useState<LinhaBancada[]>([]);
  const [loadingAmostras, setLoadingAmostras] = useState(false);
  const [salvando, setSalvando] = useState<Record<string, boolean>>({});
  const [jaFiltrou, setJaFiltrou] = useState(false);

  // ── Busca de laudos (debounced) ────────────────────────────────────────────
  const handleLaudoInput = useCallback((_: React.SyntheticEvent, value: string) => {
    setLaudoInput(value);

    if (!value || value.trim().length < 2) {
      setLaudoOpcoes([]);
      return;
    }

    if (laudoTimer.current) clearTimeout(laudoTimer.current);
    laudoTimer.current = setTimeout(async () => {
      if (laudoAbort.current) laudoAbort.current.abort();
      laudoAbort.current = new AbortController();
      setLoadingLaudos(true);
      try {
        const lista = await laudoService.buscarPorCodigo(
          value.trim(),
          laudoAbort.current.signal,
        );
        setLaudoOpcoes(lista);
      } catch {
        // busca cancelada ou erro silencioso
      } finally {
        setLoadingLaudos(false);
      }
    }, 300);
  }, []);

  const handleLaudoChange = useCallback(
    (_: React.SyntheticEvent, laudo: Laudo | null) => {
      setLaudoSelecionado(laudo);
      setEquipamento("");
      setElemento("");
      setBaterias([]);
      setBateriaSelecionada(null);
      setLinhas([]);
      setJaFiltrou(false);
    },
    [],
  );

  // ── Carrega baterias ao mudar equipamento+elemento ─────────────────────────
  const carregarBaterias = useCallback(
    async (eq: Equipamento, el: Elemento) => {
      setLoadingBaterias(true);
      setBaterias([]);
      setBateriaSelecionada(null);
      setLinhas([]);
      setJaFiltrou(false);
      try {
        const lista = await calibracaoService.listarBaterias(eq, el);
        setBaterias(lista);
      } catch {
        showError("Erro ao carregar baterias disponíveis.");
      } finally {
        setLoadingBaterias(false);
      }
    },
    [showError],
  );

  const handleSetEquipamento = useCallback(
    (eq: Equipamento | "") => {
      setEquipamento(eq);
      setElemento("");
      setBaterias([]);
      setBateriaSelecionada(null);
      setLinhas([]);
      setJaFiltrou(false);
    },
    [],
  );

  const handleSetElemento = useCallback(
    (el: Elemento | "") => {
      setElemento(el);
      setBateriaSelecionada(null);
      setLinhas([]);
      setJaFiltrou(false);
      if (equipamento && el) {
        void carregarBaterias(equipamento as Equipamento, el as Elemento);
      } else {
        setBaterias([]);
      }
    },
    [equipamento, carregarBaterias],
  );

  // ── Carrega amostras ───────────────────────────────────────────────────────
  const handleFiltrar = useCallback(async () => {
    if (!bateriaSelecionada) {
      showError("Selecione uma bateria antes de carregar.");
      return;
    }
    setLoadingAmostras(true);
    setLinhas([]);
    setJaFiltrou(true);
    try {
      const amostras = await entradaLoteService.buscarAmostrasPendentes(
        bateriaSelecionada.id,
        laudoSelecionado?.id,
      );
      setLinhas(
        amostras.map((a) => ({
          ...a,
          equipamento: bateriaSelecionada.equipamento,
          elemento: bateriaSelecionada.elemento as Elemento,
          leitura_bruta: "",
          fator_diluicao: "",
          resultado_preview: null,
          status: "pendente",
        })),
      );
    } catch {
      showError("Erro ao carregar amostras.");
    } finally {
      setLoadingAmostras(false);
    }
  }, [bateriaSelecionada, laudoSelecionado, showError]);

  // ── Salva leitura ao editar célula ─────────────────────────────────────────
  const handleProcessRowUpdate = useCallback(
    async (
      newRow: LinhaBancada,
      oldRow: LinhaBancada,
    ): Promise<LinhaBancada> => {
      if (!bateriaSelecionada) return oldRow;

      const leituraNum = parseFloat(
        normalizeDecimalInput(newRow.leitura_bruta),
      );
      if (isNaN(leituraNum)) return newRow;

      const precisaFd = REQUER_VOLUMES.includes(bateriaSelecionada.equipamento);
      const fdNum = newRow.fator_diluicao
        ? parseFloat(normalizeDecimalInput(newRow.fator_diluicao))
        : undefined;

      if (precisaFd && fdNum === undefined) return newRow;

      setSalvando((prev) => ({ ...prev, [newRow.n_lab]: true }));

      try {
        const resposta = await entradaLoteService.salvarLeitura({
          analise: newRow.id,
          bateria: bateriaSelecionada.id,
          leitura_bruta: leituraNum,
          ...(fdNum !== undefined && { fator_diluicao: fdNum }),
        });

        const usaCurva = !SEM_CURVA_CALIBRACAO.includes(bateriaSelecionada.equipamento);
        const semCurva = usaCurva && bateriaSelecionada.coeficiente_angular_a === null;
        const linhaAtualizada: LinhaBancada = {
          ...newRow,
          resultado_preview: semCurva ? null : (resposta.resultado_calculado ?? null),
          status: "salvo",
        };

        setLinhas((prev) =>
          prev.map((l) => (l.n_lab === newRow.n_lab ? linhaAtualizada : l)),
        );
        showSuccess(`Leitura de ${newRow.n_lab} salva.`);
        return linhaAtualizada;
      } catch (err) {
        const linhaComErro: LinhaBancada = { ...oldRow, status: "erro" };
        setLinhas((prev) =>
          prev.map((l) => (l.n_lab === oldRow.n_lab ? linhaComErro : l)),
        );
        showApiError(err);
        return linhaComErro;
      } finally {
        setSalvando((prev) => ({ ...prev, [newRow.n_lab]: false }));
      }
    },
    [bateriaSelecionada, showSuccess, showApiError],
  );

  return {
    // laudo
    laudoInput,
    laudoSelecionado,
    laudoOpcoes,
    loadingLaudos,
    handleLaudoInput,
    handleLaudoChange,
    // equipamento / elemento
    equipamento,
    handleSetEquipamento,
    elemento,
    handleSetElemento,
    // bateria
    baterias,
    loadingBaterias,
    bateriaSelecionada,
    setBateriaSelecionada,
    // bancada
    jaFiltrou,
    linhas,
    loadingAmostras,
    salvando,
    handleFiltrar,
    handleProcessRowUpdate,
  };
}
