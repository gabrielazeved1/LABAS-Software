import { z } from "zod";
import type { Equipamento, Elemento } from "../types/calibracao";

export const bateriaSchema = z.object({
  equipamento: z.enum(["AA", "FC", "ES", "TI", "PH"] as const),
  elemento: z.string().min(1, "Selecione o elemento"),
  volume_solo: z.coerce.number().nullable().optional(),
  volume_extrator: z.coerce.number().nullable().optional(),
  leitura_branco: z.coerce.number().nullable().optional(),
  ativo: z.boolean(),
});

export const pontoSchema = z.object({
  concentracao: z.coerce.number({ message: "Coloque um valor válido" }),
  absorvancia: z.coerce.number({ message: "Coloque um valor válido" }),
});

export type BateriaForm = z.infer<typeof bateriaSchema>;
export type PontoForm = z.infer<typeof pontoSchema>;
