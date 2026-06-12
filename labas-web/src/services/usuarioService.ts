import { api } from "./api";

export interface Tecnico {
  id: number;
  username: string;
  email: string;
  nome: string;
  date_joined: string;
}

export interface TecnicoCriarPayload {
  username: string;
  email: string;
  nome: string;
  password: string;
}

const listar = async (): Promise<Tecnico[]> => {
  const { data } = await api.get<{ results: Tecnico[] } | Tecnico[]>("tecnicos/");
  return Array.isArray(data) ? data : data.results;
};

const criar = async (payload: TecnicoCriarPayload): Promise<Tecnico> => {
  const { data } = await api.post<Tecnico>("tecnicos/", payload);
  return data;
};

const remover = async (id: number): Promise<void> => {
  await api.delete(`tecnicos/${id}/`);
};

export const usuarioService = { listar, criar, remover };
