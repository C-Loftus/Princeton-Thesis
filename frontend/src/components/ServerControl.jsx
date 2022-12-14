import {
  Alert,
  AlertIcon,
  Fade,
  Input,
  Select,
  useDisclosure,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

export default function ServerForm(props) {

  const { isOpen, onToggle } = useDisclosure();
  const { isRunning, setIsRunning, requiredClients, setRequiredClients } = props;
  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { errors },
  } = useForm({
    defaultValues: {
      strategy: "FedAvg",
      clients: 4,
    },
  });


  const onSubmit = () => {
    const strategy = getValues("strategy");
    const clients = getValues("clients");
    setRequiredClients(clients);
    const query = isRunning ? "stop" : "start";
    fetch(`api/${query}?strategy=${strategy}&clients=${clients}`)
      .then((res) => {
        if (res.ok) {
          setIsRunning(!isRunning);
        }
        res.json();
      })
      .catch((err) => {
        console.log(err);
      });
    reset();
  };

  useEffect(() => {
    fetch(`/api/running`)
      .then((response) => response.json())
      .then((data) => {
        console.log(`is running?: ${data}`);
        setIsRunning(data.detail);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [isRunning, setIsRunning]);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {!isRunning && (
        <div>
          <h5> Input the Strategy for Training </h5>
          <Select
            {...register("strategy", { required: true })}
            aria-invalid={errors.strategy ? "true" : "false"}
          >
            <option value="FedAvg">FedAvg</option>
            <option value="FedAvgM">FedAvgM</option>
            <option value="QFedAvg">QFedAvg</option>
            <option value="FaultTolerantFedAvg">FaultTolerantFedAvg</option>
            <option value="FedOpt">FedOpt</option>
            <option value="FedAdagrad">FedAdagrad</option>
            <option value="FedAdam">FedAdam</option>
            <option value="FedYogi">FedYogi</option>
          </Select>

          <h5> Input the number of clients to require </h5>
          <Input
            type="clients"
            {...register("clients", { required: !isRunning ? true : false })}
          />
          {errors.clients?.type === "required" && (
            <Fade in={isOpen}>
              <Alert status="error">
                <AlertIcon />
                You need to input the number of clients
              </Alert>
            </Fade>
          )}
        </div>
      )}
      <Input
        type="submit"
        onClick={onToggle}
        value={`Turn the Federate Learning Server ${isRunning ? "off" : "on"}`}
      />
    </form>
  );
}
