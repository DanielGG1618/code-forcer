import { useForm } from "react-hook-form";
import Form from "../../ui/Form";
import Heading from "../../ui/Heading";
import Input from "../../ui/Input";
import Button from "../../ui/Button";
import FormElement from "../../ui/FormElement";
import { uploadSingleHandle } from "../../api/handles";
import { useState } from "react";
import SpinnerMini from "../../ui/SpinnnerMini";
import toast from "react-hot-toast";

export default function FormHandleUpdate() {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm();

  const [isGetting, setIsGetting] = useState(false);
  const onSubmit = function (data) {
    setIsGetting(true);
    data.handle = data.handle.trim();
    data.email = data.email.trim();

    uploadSingleHandle(data)
      .then((res) => {
        toast.success(`Successfully ${res.status == 204 ? "updated" : "created"}!`);
        reset();
      })
      .catch((err) => {
        toast.error(err.message);
      })
      .finally(() => {
        setIsGetting(false);
      });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Heading as="h2">Update single handle</Heading>
      <FormElement
        label="Student's email"
        error={errors?.email?.message}
        text={"@innopolis.university"}
      >
        <Input
          disabled={isGetting}
          placeholder="s.razmakhov"
          {...register("email", {
            required: "This field is required",
            setValueAs: (val) => val + "@innopolis.university",
          })}
        />
      </FormElement>
      <FormElement label="Handle on CodeForces" error={errors?.handle?.message}>
        <Input
          disabled={isGetting}
          placeholder="pussycat05"
          {...register("handle", { required: "This field is required" })}
        />
      </FormElement>
      <Button disabled={isGetting} type="submit">
        {isGetting ? <SpinnerMini /> : "Submit"}
      </Button>
    </Form>
  );
}
