import { useForm } from "react-hook-form";
import { useEffect } from "react";

export default function ServerForm(props) {
  const { isRunning, setIsRunning } = props;
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      strategy: "FedAvg",
    },
  });

  const onSubmit = (d) => {
    const query = isRunning ? "stop" : "start";
    fetch(query)
      .then((res) => {
        if (res.ok) {
          setIsRunning(!isRunning);
        }
        res.json();
      })
      .then((data) => {
        console.log(data.message);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(() => {
    fetch(`/running`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data.detail);
        setIsRunning(data.detail);
      });
  }, [isRunning]);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <h5> Input the Strategy for Training </h5>

      <select {...register("strategy", { required: true })}>
        <option value="FedAvg">FedAvg</option>
        <option value="FedAvgM">FedAvgM</option>
        <option value="QFedAvg">QFedAvg</option>
        <option value="FaultTolerantFedAvg">FaultTolerantFedAvg</option>
        <option value="FedOpt">FedOpt</option>
        <option value="FedAdagrad">FedAdagrad</option>
        <option value="FedAdam">FedAdam</option>
        <option value="FedYogi">FedYogi</option>
      </select>
      {errors.strategy && <span>This field is required</span>}

      <h5> Input the number of clients to require </h5>
      <input type="clients" {...register("clients", { min: 5, max: 99 })} />
      {errors.clients && <span>This field is required</span>}
      <br/>
      <br/>

      <input type="submit" value={`Turn the Server ${isRunning ? "off" : "on"}`}/>
    </form>
  );
}
