import { useForm } from "react-hook-form";
import { useEffect } from "react";

export default function ServerForm(props) {
  const { isRunning, setIsRunning } = props;
  const {
    register,
    handleSubmit,
    reset,
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
      reset();
  };

  useEffect(() => {
    fetch(`/running`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data.detail);
        setIsRunning(data.detail);
      });
  }, [isRunning, setIsRunning]);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {!isRunning && (
        <div>
        <h5> Input the Strategy for Training </h5>
        <select {...register("strategy", { required: true })} aria-invalid={errors.strategy ? "true" : "false"} >
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
        <input type="clients" {...register("clients", { required: !isRunning ? true: false })} />
        {errors.clients?.type === 'required' && <p role="alert">Client number is required</p>}
        <br/>
        <br/>
        </div>
      )
      
      }
      
      <input type="submit" value={`Turn the Server ${isRunning ? "off" : "on"}`}/>
    </form>
  );
}
