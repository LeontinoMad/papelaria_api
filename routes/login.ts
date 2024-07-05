import jwt from "jsonwebtoken"
import { PrismaClient } from "@prisma/client"
import { Router } from "express"
import bcrypt from 'bcrypt'

const prisma = new PrismaClient()
const router = Router()

router.post("/", async (req, res) => {
  const { email, senha } = req.body

  const mensaPadrao = "Login ou senha incorretos"
  
  if (!email || !senha) {
    res.status(400).json({ erro: mensaPadrao })
    return
  }
  
  try {
    const usuario = await prisma.usuario.findFirst({
      where: { email }
    })

    if (usuario == null) {
      res.status(400).json({ erro: mensaPadrao })
      return
    }

    // Impede a realização do login caso o usuário esteja bloequeado
    // if (usuario.tentativa != null && usuario.tentativa >= 3) {
    //     res.status(400).json({ erro: "Número de tentativas inválidas máximas alcançadas. Por favor, aguarde até ser liberado um novo login." })
    //     return
    //   } 

    // se o e-mail existe, faz-se a comparação dos hashs
    if (bcrypt.compareSync(senha, usuario.senha)) {
      // se confere, gera e retorna o token
      const token = jwt.sign({
        userLogadoId: usuario.id,
        userLogadoNome: usuario.nome
      },
      process.env.JWT_KEY as string,
      { expiresIn: "1h" })

      // Atualiza os campos de condição para "bloqueio"
      await prisma.usuario.update({
        where: { id: usuario.id },
        data: { tentativa: 0, ultimaTentativa: new Date() },
      })
      
      res.status(200).json({
        id: usuario.id,
        nome: usuario.nome,
        email: usuario.email,
        token
      })
    } else {
      // Registra a primeira tentativa de login falho:
      if (usuario.tentativa == 0){
        await prisma.usuario.update({
          where: { id: usuario.id },
          data: { ultimaTentativa: new Date() },
        })
      }

      const bloqueio = await prisma.usuario.update({
        where: { id: usuario.id },
        data: { tentativa: { increment: 1 } },
      })

      await prisma.log.create({
        data: { 
          descricao: "Tentativa de Acesso Inválida", 
          complemento: `Funcionário: ${usuario.email}`,
          usuarioId: usuario.id
        }
      })
      
      if (usuario.tentativa != null && usuario.tentativa >= 3) {
        res.status(400).json({ erro: "Número de tentativas inválidas máximas alcançadas. Por favor, aguarde até ser liberado um novo login." })
      } else {
        res.status(400).json({ erro: mensaPadrao })
      }
    }
  } catch (error) {
    res.status(400).json(error)
  }
})

export default router

// {
// "email": "",
// "senha": ""
// }
