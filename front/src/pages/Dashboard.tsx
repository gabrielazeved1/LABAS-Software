import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { FileText, Users, ArrowRight, Calendar } from "lucide-react";
import { useNavigate } from "react-router-dom";

// Dados mockados para demonstração
const ultimosLaudos = [
  { id: 1, produtor: "João Silva", data: "24/01/2026", status: "Concluído" },
  { id: 2, produtor: "Maria Santos", data: "23/01/2026", status: "Concluído" },
  { id: 3, produtor: "Carlos Oliveira", data: "22/01/2026", status: "Pendente" },
  { id: 4, produtor: "Ana Costa", data: "21/01/2026", status: "Concluído" },
  { id: 5, produtor: "Pedro Lima", data: "20/01/2026", status: "Concluído" },
];

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold text-foreground">Início</h1>
        <p className="text-muted-foreground mt-1">O que você deseja fazer hoje?</p>
      </div>
      
      {/* Cards de Ação */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="group cursor-pointer hover:shadow-lg transition-all hover:border-primary" onClick={() => navigate("/laudos/gerar")}>
          <CardContent className="p-6">
            <div className="flex items-start justify-between">
              <div className="space-y-3">
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <FileText className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-foreground">Gerar Laudo</h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    Crie um novo laudo de análise de solo
                  </p>
                </div>
              </div>
              <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
            </div>
          </CardContent>
        </Card>

        <Card className="group cursor-pointer hover:shadow-lg transition-all hover:border-primary" onClick={() => navigate("/produtores/cadastrar")}>
          <CardContent className="p-6">
            <div className="flex items-start justify-between">
              <div className="space-y-3">
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Users className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-foreground">Cadastrar Produtor</h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    Adicione um novo produtor ao sistema
                  </p>
                </div>
              </div>
              <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Últimos Laudos */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-lg">Últimos Laudos Gerados</CardTitle>
          <Button variant="ghost" size="sm" onClick={() => navigate("/laudos")} className="text-primary">
            Ver todos
            <ArrowRight className="h-4 w-4 ml-1" />
          </Button>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Produtor</TableHead>
                <TableHead>Data</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {ultimosLaudos.map((laudo) => (
                <TableRow key={laudo.id}>
                  <TableCell className="font-medium">{laudo.produtor}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Calendar className="h-4 w-4" />
                      {laudo.data}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant={laudo.status === "Concluído" ? "default" : "secondary"}>
                      {laudo.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm">
                      Visualizar
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
