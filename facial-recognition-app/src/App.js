import "./App.css";
import React, { useState } from "react";
import * as uuid from "uuid";

function App() {
  const [image, setImage] = useState("");
  const [uploadResultMessage, setUploadResultMessage] = useState(
    "Por favor, sube una imagen para buscar si ese menor de edad tiene una Alerta Amber."
  );
  const [imgName, setImageName] = useState("ObtenerFotoDesaparecido.jpeg");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

function sendImage(e) {
  e.preventDefault();
  setImageName(image.name);
  const ImageName = uuid.v4();
  fetch(
    `https://asb99ir0ef.execute-api.us-east-1.amazonaws.com/prueba/itam-proyecto-saraluz-test/${ImageName}.jpeg`,
    {
      method: "PUT",
      mode: "no-cors",
      headers: {
        "Content-Type": "image/jpeg",
      },
      body: image,
    }
  )
    .then(async (response) => {
      if (response.ok) {
        const authResponse = await authenticate(ImageName);
        if (authResponse.Message === "Success") {
          setIsAuthenticated(true);
          setUploadResultMessage(
            `El menor de edad de la foto tiene la Alerta Amber numero ${authResponse["reporte"]}.`
          );
        } else {
          setIsAuthenticated(false);
          setUploadResultMessage(
            "El menor de edad de la foto no tiene una Alerta Amber."
          );
        }
      } else {
        console.error("Error uploading image:", response.statusText);
        setIsAuthenticated(false);
        setUploadResultMessage(
          "Hubo un error al subir la imagen, por favor intenta de nuevo."
        );
      }
    })
    .catch((error) => {
      console.error("Hubo un error al subir la imagen:", error);
      setIsAuthenticated(false);
      setUploadResultMessage(
        "Hubo un error al subir la imagen, por favor intenta de nuevo."
      );
    });
}


  async function authenticate(imageName) {
    const requestUrl =
      `https://asb99ir0ef.execute-api.us-east-1.amazonaws.com/prueba/amber?` +
      new URLSearchParams({
        objectKey: `${imageName}.jpeg`,
      });
    try {
      const response = await fetch(requestUrl, {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        console.error("Error al autenticar la imagen:", response.statusText);
        return { Message: "Error" };
      }
    } catch (error) {
      console.error("Hubo un error al autenticar la imagen:", error);
      return { Message: "Error" };
    }
  }

  return (
    <div className="App">
      <h2>Consulta de fotos en los reportes de Alerta Amber en Chiapas</h2>
      <form onSubmit={sendImage}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />
        <button type="submit">Revisar</button>
      </form>

      <div className={isAuthenticated ? "success" : "failure"}>
        {uploadResultMessage}
      </div>

      {/* <img src={require(`./../../data/test/${imgName}`)} alt="Imagen subida" height={250} width={250} /> */}
    </div>
  );
}

export default App;
