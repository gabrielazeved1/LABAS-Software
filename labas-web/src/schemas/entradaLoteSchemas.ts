import { z } from "zod";
import { REQUER_VOLUMES } from "../config/calibracaoConstants";
import type { Equipamento } from "../types/calibracao";

/**
 * Schema base para uma linha da bancada.
 * O superRefine torna fator_diluicao obrigatório para AA, FC e ES,
 * espelhando a regra do clean() de LeituraEquipamento no backend.
 */
export const leituraSchema = z
  .object({
    leitura_bruta: z.coerce
      .number({ invalid_type_error: "Informe a leitura" })
      .positive("A leitura deve ser positiva"),
    fator_diluicao: z.coerce
      .number({ invalid_type_error: "Informe o fator de diluição" })
      .positive("O fator deve ser positivo")
      .optional(),
    equipamento: z.enum(["AA", "FC", "ES", "TI", "PH"] as const),
  })
  .superRefine((data, ctx) => {
    if (
      REQUER_VOLUMES.includes(data.equipamento as Equipamento) &&
      data.fator_diluicao === undefined
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ["fator_diluicao"],
        message: "Fator de diluição obrigatório para este equipamento",
      });
    }
  });

export type LeituraForm = z.infer<typeof leituraSchema>;
