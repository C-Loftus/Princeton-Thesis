import { Formik } from "formik";
import { useFormik } from 'formik';
import React from 'react';

export default function ServerForm(props) {
  const formik = useFormik({
    initialValues: {
      strategy: "FedAvg",
      clients: 5,
    },
    onSubmit: (values) => {
      alert(JSON.stringify(values, null, 2));
    },
  });

  console.log(formik.values);

  return (
    <form onSubmit={formik.handleSubmit}>
      <h5> Select the Strategy to use </h5>
      <select value={formik.values.strategy} onChange={formik.handleChange}>
        <option value="FedAvg">FedAvg</option>
        <option value="FedAvgM">FedAvgM</option>
        <option value="QFedAvg">QFedAvg</option>
        <option value="FaultTolerantFedAvg">FaultTolerantFedAvg</option>
        <option value="FedOpt">FedOpt</option>
        <option value="FedAdagrad">FedAdagrad</option>
        <option value="FedAdam">FedAdam</option>
        <option value="FedYogi">FedYogi</option>
      </select>

      <h5> Input the number of clients to require </h5>
      <input
        type="number"
        id="quantity"
        name="quantity"
        min="1"
        max="100"
        placeholder="5"
        value={formik.values.clients}
        onChange={formik.handleChange}
      ></input>
    </form>
  );
}
