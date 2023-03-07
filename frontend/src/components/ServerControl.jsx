import {
  Alert,
  AlertIcon,
  Fade,
  Input,
  Select,
  useDisclosure,
  Divider,
  Checkbox,
  Text,
  Badge,
  Textarea,
  Tooltip,
  Button,
  HStack,
  Spacer
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { command_list } from "./default_commands";

export default function ServerForm(props) {
  const { isOpen, onToggle } = useDisclosure();
  const { isRunning, setIsRunning, requiredClients, setRequiredClients } =
    props;
  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { errors },
  } = useForm({
    defaultValues: {
      strategy: "FedAvgM",
      clients: 4,
      commands: command_list,
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
          <HStack>

          <Tooltip hasArrow label=" These labels need to be present in the users' Talon training data. The final model will only include these labels." paddingTop={12} paddingBlock={10}>
          <Badge ml="1" fontSize="0.8em" colorScheme="green">
              ?
            </Badge>
          </Tooltip>
          <h5> Input the Strategy for Training </h5>

          </HStack>
          <Select
            {...register("strategy", { required: true })}
            aria-invalid={errors.strategy ? "true" : "false"}
          >
            <option value="FedAvg">FedAvg</option>
            <option value="FedAvgM">Fast Convergence: FedAvgM</option>
            <option value="QFedAvg">QFedAvg</option>
            <option value="FaultTolerantFedAvg">FaultTolerantFedAvg</option>
            <option value="FedOpt">FedOpt</option>
            <option value="FedAdagrad">FedAdagrad</option>
            <option value="FedAdam">FedAdam</option>
            <option value="FedYogi">FedYogi</option>
          </Select>
          <Text paddingTop={12} />

          <HStack>
          
          <Tooltip hasArrow label=" These labels need to be present in the users' Talon training data. The final model will only include these labels." paddingTop={12}>
          <Badge ml="1" fontSize="0.8em" colorScheme="green">
              ?
            </Badge>
          </Tooltip>
        
          <h5> Input the list of commands you want in the final model </h5>
          </HStack>
          <Textarea
            padding={3}
            type="commands"
            {...register("commands", { required: false })}
          />


      <Text paddingTop={12} />
          <HStack>
          <Tooltip hasArrow label="4 is the minimum. The more the better if you can find enough people.">
          <Badge ml="1" fontSize="0.8em" colorScheme="green">
              ?
            </Badge>
          </Tooltip>



          <h5>     Input the number of clients to require </h5>
          </HStack>
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
        value={`Turn the Federated Learning Server ${isRunning ? "off" : "on"}`}
      />
    </form>
  );
}
