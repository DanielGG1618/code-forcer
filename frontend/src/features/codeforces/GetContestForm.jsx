import { useForm } from "react-hook-form";
import { useLocalStorageState } from "../../hooks/useLocalStorage.js";
import Form from "../../ui/Form.jsx";
import Input from "../../ui/Input.jsx";
import FormElement from "../../ui/FormElement.jsx";
import Button from "../../ui/Button.jsx";
import { useNavigate, useNavigation } from "react-router-dom";
import SpinnerMini from "../../ui/SpinnnerMini.jsx";
import { useEffect } from "react";

function GetContestForm() {
  const [id, setId] = useLocalStorageState(null, "id");
  const [api, setApi] = useLocalStorageState(null, "api");
  const [secret, setSecret] = useLocalStorageState(null, "secret");

  const navigate = useNavigate();
  const navigation = useNavigation();

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm({
    defaultValues: {
      contestID: id,
      APIKey: api,
      secretKey: secret,
    },
  });

  useEffect(() => {
    const subscription = watch((value) => {
      setId(value.contestID);
      setApi(value.APIKey);
      setSecret(value.secretKey);
    });
    return () => subscription.unsubscribe();
  }, [watch, setId, setApi, setSecret]);

  const onSubmit = function (data) {
    // Getting values from form
    let { contestID, APIKey, secretKey } = data;
    // Convert URL to id
    if (contestID.startsWith("http")) {
      contestID = contestID.match(/.*contest\/([0-9]*)/)[1];
    }

    // Setting values in local storage
    setId(contestID);
    setApi(APIKey);
    setSecret(secretKey);

    if (api && secret) {
      navigate(`${contestID}`);
    }
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <FormElement label="Contest URL" error={errors?.contestID?.message}>
        <Input
          placeholder="ID or full link"
          disabled={navigation.state !== "idle"}
          {...register("contestID", { required: "This field is required" })}
        />
      </FormElement>
      <FormElement
        label="Codeforces API"
        disabled={navigation.state !== "idle"}
        error={errors?.APIKey?.message || errors?.secretKey?.message}
      >
        <Input
          placeholder="API Key"
          disabled={navigation.state !== "idle"}
          {...register("APIKey", { required: "These fields are required" })}
        />
        <Input
          placeholder={"Secret Key"}
          disabled={navigation.state !== "idle"}
          {...register("secretKey", {
            required: "These fields are required",
          })}
        />
      </FormElement>
      <Button disabled={navigation.state !== "idle"} type="submit">
        {navigation.state !== "idle" ? <SpinnerMini /> : "Submit"}
      </Button>
    </Form>
  );
}

export default GetContestForm;
