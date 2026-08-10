/*
 * Tipos relacionados à autenticação, incluindo o par de tokens JWT, payloads para login e registro, e a interface do usuário autenticado.
 */
export interface TokenPair {
  access: string;
  refresh: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}


export interface AuthUser {
  id: number;
  username: string;
  email: string;
  is_staff: boolean;
}
