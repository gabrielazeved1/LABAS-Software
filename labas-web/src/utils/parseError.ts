export function parseError(error: any): string {
  if (error?.response?.data) {
    const data = error.response.data;

    // DRF format: { campo: ["mensagem"] }
    if (typeof data === "object") {
      return Object.values(data).flat().join(" ");
    }

    if (typeof data === "string") return data;
  }

  return "Erro inesperado";
}