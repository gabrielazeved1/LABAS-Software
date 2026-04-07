import { z } from "zod";

const dateSchema = z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Data inválida");
const optionalDate = z.union([dateSchema, z.literal("")]);

const nullableNumber = z
  .union([z.coerce.number(), z.literal("")])
  .transform((value) => (value === "" ? null : value));

/** Schema para criar/editar uma AnaliseSolo vinculada a um Laudo. */
export const analiseSchema = z.object({
  n_lab: z
    .string()
    .min(1, "N° do laudo é obrigatório")
    .regex(/^\d{4}\/\d{3}$/, "Use o formato AAAA/NNN"),
  referencia: z.string().optional(),
  data_entrada: dateSchema,
  data_saida: optionalDate,
  ativo: z.boolean().default(true),
  ph_agua: nullableNumber.optional(),
  ph_cacl2: nullableNumber.optional(),
  ph_kcl: nullableNumber.optional(),
  p_m: nullableNumber.optional(),
  p_r: nullableNumber.optional(),
  p_rem: nullableNumber.optional(),
  mo: nullableNumber.optional(),
  s: nullableNumber.optional(),
  b: nullableNumber.optional(),
  k: nullableNumber.optional(),
  na: nullableNumber.optional(),
  ca: nullableNumber.optional(),
  mg: nullableNumber.optional(),
  cu: nullableNumber.optional(),
  fe: nullableNumber.optional(),
  mn: nullableNumber.optional(),
  zn: nullableNumber.optional(),
  al: nullableNumber.optional(),
  h_al: nullableNumber.optional(),
  areia: nullableNumber.optional(),
  argila: nullableNumber.optional(),
  silte: nullableNumber.optional(),
});

export type AnaliseFormInput = z.input<typeof analiseSchema>;
export type AnaliseForm = z.output<typeof analiseSchema>;
