import "dotenv/config";
import express from "express";
import filesRoutes from "./routes/files.js";
import { exec, spawn } from "child_process"; // pour executer les commandes ligne
import { env } from "process";

export const app = express();
const port = process.env.PORT || 3001;

if (process.env.STATIC) app.use("/static", express.static(process.env.STATIC));
if (process.env.STATIC) app.use("/files", filesRoutes);

app.use(express.json());
app.put("/", (req, res) => {
  const { input = "walking.avi" } = req.body;
  const output = "result-" + Date.now().toString();
  const commande = spawn(
    "python ",
    [
      "./scripts/BackgroundSub.py",
      "-i",
      "./public/" + input,
      "-o",
      "./public/" + output,
    ],
    { shell: true}
  );

  commande.stdout.on("data", (data) => {
    res.write(data);
  });

  commande.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  commande.on("close", (code) => {
    res.end("100%");
  });
});

app.use((err, req, res, next) => {
  const error =
    err.message && err.name
      ? {
          name: err.name,
          message: err.message,
        }
      : {
          name: "unhandled_error",
          message: "Encountered unhandled error please try again.",
        };
  res.status(err.status || 422).send(error);
});
app.use("*", (req, res, next) => {
  res.status(404).json({
    name: "resource_not_found",
    message: "Resource not found.",
  });
});
app.listen(port, () => console.log(`Server running on port: ${port}`));
