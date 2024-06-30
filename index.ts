import express from "express";
const app = express();
const port = 3000;
import cors from "cors";

import produtosRoutes from "./routes/produtos";
import usuariosRoutes from "./routes/usuarios";
import loginRoutes from "./routes/login";

app.use(express.json());
app.use(cors());
app.use("/produtos", produtosRoutes);
app.use("/usuarios", usuariosRoutes);
app.use("/login", loginRoutes);

app.get("/", (req, res) => {
  res.send("API de Papelaria: Controle de produtos");
});

app.listen(port, () => {
  console.log(`Servidor rodando na porta: ${port}`);
});
