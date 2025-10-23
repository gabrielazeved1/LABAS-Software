'use client'

import { FormInput } from "@/components/form-components/form-input";
import { Card, CardAction, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import { FormProvider, useForm } from "react-hook-form";

interface Props {
  username: string;
  password: string;
}


export default function Home() {
    const form = useForm<Props>();

      const onSubmit = (data: Props) => {
    console.log(data);
  };

  return (
    <main className="bg-linear-to-br from-yellow-50 via-orange-50 to-red-50 min-h-screen w-full flex  md:flex-row">
       <FormProvider {...form}>
        <div className="flex items-center justify-center w-full md:w-1/2">
          <Card className="w-100 shadow-lg">
            <CardHeader>
              <CardTitle>Entrar</CardTitle>
              <CardDescription>Entre com sua conta para obter todas as funcionalidades</CardDescription>
              <CardAction>Criar conta</CardAction>
            </CardHeader>
            <CardContent>
              <form className=" flex flex-col gap-4" onSubmit={form.handleSubmit(onSubmit)}>

              <FormInput
                control={form.control}
                label="Usuário"
                name="username"
                placeholder="Aaaaaa"
              />
              <FormInput
                control={form.control}
                label="Senha"
                name="password"
                placeholder="Aaaaaa"
                type="password"
              />
              </form>
            </CardContent>
            <CardFooter>
              <p>Entrar sem login</p>
            </CardFooter>
          </Card>
        </div>
        

        <div className="relative hidden md:block w-1/2">
          <Image
            src="/login.webp"
            alt="Tela de login"
            fill
            style={{ objectFit: "cover" }}
            sizes="100vw"
          />
        </div>
      </FormProvider>
    </main>
  );
}
