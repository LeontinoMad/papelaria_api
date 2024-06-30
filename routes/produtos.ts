import { PrismaClient } from "@prisma/client";
import { Router } from "express";

import { verificaToken } from "../middewares/verificaToken";

const prisma = new PrismaClient();

async function main() {
  /***********************************/
  /* SOFT DELETE MIDDLEWARE */
  /***********************************/
  prisma.$use(async (params, next) => {
    // Check incoming query type
    if (params.model == "Produto") {
      if (params.action == "delete") {
        // Delete queries
        // Change action to an update
        params.action = "update";
        params.args["data"] = { deleted: true };
      }
    }
    return next(params);
  });
}
main();

const router = Router();

router.get("/", async (req, res) => {
  try {
    const produtos = await prisma.produto.findMany({
      where: { deleted: false },
    });
    res.status(200).json(produtos);
  } catch (error) {
    res.status(400).json(error);
  }
});

router.post("/", verificaToken, async (req: any, res) => {
  // dados que são fornecidos no corpo da requisição
  const { nome, marca, categoria, preco } = req.body;

  // dado que é acrescentado pelo Token (verificaToken) no req
  const { userLogadoId } = req;

  if (!nome || !marca || !categoria || !preco) {
    res.status(400).json({ erro: "Informe nome, marca, categoria e preco" });
    return;
  }

  try {
    const produto = await prisma.produto.create({
      data: { nome, marca, categoria, preco, usuarioId: userLogadoId },
    });
    res.status(201).json(produto);
  } catch (error) {
    res.status(400).json(error);
  }
});

router.delete("/:id", verificaToken, async (req, res) => {
  const { id } = req.params;

  try {
    const produto = await prisma.produto.delete({
      where: { id: Number(id) },
    });
    res.status(200).json(produto);
  } catch (error) {
    res.status(400).json(error);
  }
});

router.put("/:id", verificaToken, async (req, res) => {
  const { id } = req.params;
  const { nome, marca, categoria, preco } = req.body;

  if (!nome || !marca || !categoria || !preco) {
    res.status(400).json({ erro: "Informe nome, marca, categoria e preco" });
    return;
  }

  try {
    const produto = await prisma.produto.update({
      where: { id: Number(id) },
      data: { nome, marca, categoria, preco },
    });
    res.status(200).json(produto);
  } catch (error) {
    res.status(400).json(error);
  }
});

export default router;
