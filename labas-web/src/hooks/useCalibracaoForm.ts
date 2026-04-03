import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import {
  calibracaoService,
  type CriarBateriaPayload,
} from "../services/calibracaoService";
import { useSnackbar } from "./useSnackbar";
import { bateriaSchema, type BateriaForm } from "../schemas/calibracaoSchemas";
import {
  REQUER_VOLUMES,
  REQUER_BRANCO,
  SEM_CURVA_CALIBRACAO,
} from "../config/calibracaoConstants";
import type { Equipamento } from "../types/calibracao";

export interface LinhaRascunho {
  concentracao: string;
  absorvancia: string;
  erro: string | null;
}

const linhaVazia = (): LinhaRascunho => ({
  concentracao: "",
  absorvancia: "",
  erro: null,
});

export function useCalibracaoForm(
  initialBateriaId?: number,
  initialEquipamento?: Equipamento,
) {
  const navigate = useNavigate();
  const { showError, showSuccess } = useSnackbar();
  const [linhas, setLinhas] = useState<LinhaRascunho[]>([
    linhaVazia(),
    linhaVazia(),
    linhaVazia(),
  ]);
  const [salvandoPontos, setSalvandoPontos] = useState(false);
  const [activeStep, setActiveStep] = useState(initialBateriaId ? 1 : 0);
  const [novaBateriaId, setNovaBateriaId] = useState<number | null>(
    initialBateriaId ?? null,
  );
  const [submittingBateria, setSubmittingBateria] = useState(false);

  const bateriaForm = useForm<BateriaForm>({
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    resolver: zodResolver(bateriaSchema) as any,
    defaultValues: {
      equipamento: initialEquipamento ?? "AA",
      elemento: "",
      ativo: true,
    },
  });

  const handleCriarBateria = bateriaForm.handleSubmit(
    async (data: BateriaForm) => {
      setSubmittingBateria(true);
      try {
        const payload: CriarBateriaPayload = {
          equipamento: data.equipamento,
          elemento: data.elemento,
          ativo: data.ativo,
          volume_solo: REQUER_VOLUMES.includes(data.equipamento)
            ? (data.volume_solo ?? null)
            : null,
          volume_extrator: REQUER_VOLUMES.includes(data.equipamento)
            ? (data.volume_extrator ?? null)
            : null,
          leitura_branco: REQUER_BRANCO.includes(data.equipamento)
            ? (data.leitura_branco ?? null)
            : null,
        };
        const criada = await calibracaoService.criarBateria(payload);
        setNovaBateriaId(criada.id);
        if (SEM_CURVA_CALIBRACAO.includes(data.equipamento)) {
          showSuccess("Bateria criada com sucesso.");
          navigate("/calibracao");
        } else {
          showSuccess(
            "Bateria criada! Agora adicione os pontos de calibração.",
          );
          setActiveStep(1);
        }
      } catch {
        showError("Erro ao criar bateria. Verifique os campos obrigatórios.");
      } finally {
        setSubmittingBateria(false);
      }
    },
  );

  const handleAdicionarLinhas = (n = 1) => {
    setLinhas((prev) => [...prev, ...Array.from({ length: n }, linhaVazia)]);
  };

  const handleAtualizarLinha = (
    idx: number,
    field: "concentracao" | "absorvancia",
    value: string,
  ) => {
    setLinhas((prev) =>
      prev.map((l, i) =>
        i === idx ? { ...l, [field]: value, erro: null } : l,
      ),
    );
  };

  const handleRemoverLinha = (idx: number) => {
    setLinhas((prev) => prev.filter((_, i) => i !== idx));
  };

  const handleFinalizar = async () => {
    const bateriaId = novaBateriaId ?? initialBateriaId;
    if (!bateriaId) {
      showError("Bateria não encontrada.");
      return;
    }

    const isEmpty = (l: LinhaRascunho) =>
      l.concentracao.trim() === "" && l.absorvancia.trim() === "";
    const isPartial = (l: LinhaRascunho) =>
      (l.concentracao.trim() === "") !== (l.absorvancia.trim() === "");

    if (linhas.some(isPartial)) {
      setLinhas((prev) =>
        prev.map((l) =>
          isPartial(l)
            ? {
                ...l,
                erro: "Preencha os dois campos ou deixe a linha em branco.",
              }
            : l,
        ),
      );
      showError("Existem linhas com preenchimento incompleto.");
      return;
    }

    const pontosSalvar = linhas
      .filter((l) => !isEmpty(l))
      .map((l) => ({
        concentracao: parseFloat(l.concentracao),
        absorvancia: parseFloat(l.absorvancia),
        bateria: bateriaId,
      }));

    if (pontosSalvar.length === 0) {
      showSuccess("Calibração salva sem novos pontos.");
      navigate("/calibracao");
      return;
    }

    setSalvandoPontos(true);
    try {
      await Promise.all(
        pontosSalvar.map((p) => calibracaoService.adicionarPonto(bateriaId, p)),
      );
      showSuccess("Calibração salva com sucesso.");
      navigate("/calibracao");
    } catch {
      showError("Erro ao salvar pontos de calibração.");
    } finally {
      setSalvandoPontos(false);
    }
  };

  return {
    bateriaForm,
    linhas,
    salvandoPontos,
    activeStep,
    submittingBateria,
    setActiveStep,
    handleCriarBateria,
    handleAdicionarLinhas,
    handleAtualizarLinha,
    handleRemoverLinha,
    handleFinalizar,
  };
}
