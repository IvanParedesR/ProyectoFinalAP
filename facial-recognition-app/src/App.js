import "./App.css";
import React, { useState } from "react";
import * as uuid from "uuid";
import amberData from "./amber.json"
import _ from "lodash";

console.dir(process.env)

const justCorsURL = new URL( process.env.REACT_APP_CORSURL).href;
const AMZURL = new URL(process.env.REACT_APP_AMZNURL).href;

const amberChiapas = amberData.data

function App() {
  const [image, setImage] = useState("");
  const [uploadResultMessage, setUploadResultMessage] = useState(
    "Por favor, sube una imagen para buscar si ese menor de edad tiene una Alerta Amber."
  );
  const [reporte, setReporte] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const [isLoading, setIsloading] = useState(false);

  function sendImage(e) {
    e.preventDefault();
    const ImageNameKey = uuid.v4();
    const ImageName = `${ImageNameKey}-${image.name}`;
    setIsloading(true);
    fetch(
      `${justCorsURL}/${AMZURL}/itam-proyecto-saraluz-test/${ImageName}`,
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
      `${justCorsURL}/${AMZURL}/amber?` +
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
  let amberData = null;
  try {
    if (reporte !== "" && isAuthenticated){
      amberData = amberChiapas.find((element) => element["reporte"].includes( reporte));
      
      img = `/images/${amberData.image_file}`;
    }else img = `/images/ObtenerFotoDesaparecido.jpeg`;
  } catch (error) {
    console.error("Error al cargar la imagen:", error);
  }
  return (
    <div className="App">
      <h2 className="title1">
        Consulta de fotos en los reportes de Alerta Amber en Chiapas
      </h2>
      <form className="input-form" onSubmit={sendImage}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />
        <button type="submit">Revisar</button>
      </form>
      {isLoading && (
        <div>
          <h2>Cargando . . . </h2>
        </div>
      )}
      <div className={`results ${isAuthenticated ? "success" : "failure"}`}>
        {uploadResultMessage}
      </div>
      {isAuthenticated && (
        <div>
          <h2>Reporte de Alerta Amber</h2>
          <div className="reporte">
            {img && (
              <img src={img} alt="Imagen subida" height={250} width={250} />
            )}
            <p>Nombre: {_.startCase(amberData.nombre)}</p>
            <p>Fecha de nacimiento: {_.startCase(amberData.fecha_nac)}</p>
            <p>Edad: {_.startCase(amberData.edad)}</p>
            <p>Sexo: {_.startCase(amberData.genero)}</p>
            <p>Estatura: {_.startCase(amberData.estatura)}</p>
            <p>Peso: {_.startCase(amberData.peso)}</p>
            <p>Color de ojos: {_.startCase(amberData.color_ojos)}</p>
            <p>Color de cabello: {_.startCase(amberData.color_cabello)}</p>
            <p>Tipo de Cabello {_.startCase(amberData.tipo_cabello)}</p>
            <p>Señas particulares: {_.startCase(amberData.senas_part)}</p>

            <p>Fecha de desaparición: {_.startCase(amberData.fecha_hechos)}</p>
            <p>Lugar de desaparición: {_.startCase(amberData.lugar)}</p>
            <p>
              Resumen de los hechos:{" "}
              <b> {_.startCase(amberData.resumen_hechos)}</b>
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
