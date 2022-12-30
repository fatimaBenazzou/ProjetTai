import "dotenv/config";
import express from "express";
import filesRoutes from "./routes/files.js";
import { spawn } from "child_process"; // pour executer les commandes ligne
import cors from "cors";

export const app = express();
const port = process.env.PORT || 3001;

if (process.env.STATIC) app.use("/public", express.static(process.env.STATIC));

// cors
if (!process.env.ORIGIN && process.env.NODE_ENV !== "development")
  throw new Error("There is no Origin defined");
const origins = process.env.ORIGIN;
app.use(
  cors({
    origin: (origin, callback) => {
      const origin_accepted = origin && origin.match((origins ?? origin) + "$");

      if (origin_accepted) {
        callback(null, origin);
      } else {
        callback(new Error("Request's origin not accepted."));
      }
    },
    credentials: true,
  })
);

if (process.env.STATIC) app.use("/files", filesRoutes);

app.use(express.json());

const lancher = (script) => (req, res) => {
  const { input = "walking.mp4" } = req.params;
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Transfer-Encoding", "chunked");
  const commande = spawn(
    //creer un ss processus qui lance la commande python
    "python ",
    ["-u", "./scripts/" + script, "-i", "./public/" + input],
    { shell: true }
  );

  commande.stdout.on("data", (data) => {
    console.log(Date.now(), data.toString());
    res.write(data);
  });

  commande.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  commande.on("close", (code) => {
    res.end();
  });
};

app.get("/backgroundsub/:input", lancher("BackgroundSub.py"));
app.get("/opticalflow/:input", lancher("OpticalFlow.py"));

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
