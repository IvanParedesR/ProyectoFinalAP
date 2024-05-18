import "./App.css";
import React, { useState } from "react";
import * as uuid from "uuid";
const amber_chiapas = [
  "image_398.jpg",
  "image_626.jpg",
  "image_696.jpg",
  "image_754.jpg",
  "image_801.jpg",
  "image_828.jpg",
];

function App() {
  const [image, setImage] = useState("");
  const [uploadResultMessage, setUploadResultMessage] = useState(
    "Por favor, sube una imagen para buscar si ese menor de edad tiene una Alerta Amber."
  );
  const [imgName, setImageName] = useState("ObtenerFotoDesaparecido.jpeg");
  const [reporte, setReporte] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const [isLoading, setIsloading] = useState(false);

function sendImage(e) {
  e.preventDefault();
    const ImageNameKey = uuid.v4();
    const ImageName = `${ImageNameKey}-${image.name}`;
    setImageName(ImageName);
    setIsloading(true);
  fetch(
      `${justCorsURL}https://asb99ir0ef.execute-api.us-east-1.amazonaws.com/prueba/itam-proyecto-saraluz-test/${ImageName}`,
    {
      method: "PUT",
        mode: "cors",
      headers: {
          "Content-Type": image.type,
      },
      body: image,
    }
  )
    .then(async (response) => {
      if (response.ok) {
        const authResponse = await authenticate(ImageName);
          setIsloading(false);

          if (authResponse && authResponse.reporte) {
            setReporte(authResponse.reporte);
          setIsAuthenticated(true);
          setUploadResultMessage(
            `El menor de edad de la foto tiene la Alerta Amber numero ${authResponse["reporte"]}.`
          );
        } else {
            setReporte("");
          setIsAuthenticated(false);
          setUploadResultMessage(
            "El menor de edad de la foto no tiene una Alerta Amber."
          );
        }
      } else {
        console.error("Error uploading image:", response.statusText);
          setIsloading(false);

        setIsAuthenticated(false);
        setUploadResultMessage(
          "Hubo un error al subir la imagen, por favor intenta de nuevo."
        );
      }
    })
    .catch((error) => {
        setIsloading(false);

      console.error("Hubo un error al subir la imagen:", error);
      setIsAuthenticated(false);
      setUploadResultMessage(
        "Hubo un error al subir la imagen, por favor intenta de nuevo."
      );
    });
}

  async function authenticate(imageName) {
    const requestUrl =
      `${justCorsURL}https://asb99ir0ef.execute-api.us-east-1.amazonaws.com/prueba/amber?` +
      new URLSearchParams({
        objectKey: `${imageName}`,
      });
    try {
      const response = await fetch(requestUrl, {
        method: "GET",
        mode: "cors",
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
  let img = null;
  try {
    if (reporte !== "" && isAuthenticated)
      img = `/images/${amber_chiapas.find((element) =>
        element.includes(reporte)
      )}`;
    else img = `/images/ObtenerFotoDesaparecido.jpeg`;
  } catch (error) {
    console.error("Error al cargar la imagen:", error);
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
      {isLoading && <div>
        <h2>Cargando . . . </h2>
        </div>
        }
      <div className={isAuthenticated ? "success" : "failure"}>
        {uploadResultMessage}
      </div>

      {img && <img src={img} alt="Imagen subida" height={250} width={250} />}
    </div>
  );
}

export default App;
