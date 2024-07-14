import toast from "react-hot-toast";
import { useForm } from "react-hook-form";
import Form from "../../ui/Form";
import Heading from "../../ui/Heading";
import FileInput from "../../ui/FileInput";
import Input from "../../ui/Input";
import Button from "../../ui/Button";
import FormElement from "../../ui/FormElement";
import styled from "styled-components";
import { uploadHandlesFile } from "../../api/handles";
import { useState } from "react";
import SpinnerMini from "../../ui/SpinnnerMini";

const Error = styled.span`
  display: flex;
  justify-content: center;
  text-align: center;
  font-size: 1.4rem;
  color: var(--color-red-400);
`;

export default function FormFileUpdate() {
  const {
    register,
    handleSubmit,
    watch,
    setError,
    reset,
    formState: { errors },
  } = useForm();

  const watchFileInput = watch("file");

  const [isGetting, setIsGetting] = useState(false);
  function onSubmit({ file, link }) {
    if (file.length === 0 && link.trim().length == 0) {
      setError("neitherItem", {
        type: "manual",
        message: "You must fill out either file or link field",
      });
      return;
    }
    let responseStatus;
    setIsGetting(true);
    uploadHandlesFile(file[0])
      .then((res) => {
        responseStatus = res.status;
        return res.json();
      })
      .then((data) => {
        toast.success(
          `Successfully updated ${data.length ? data.length + " items" : ""}`,
        );
        reset();
      })
      .catch((err) => {
        toast.error(err.message);
      })
      .finally(() => {
        setIsGetting(false);
      });
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <FormElement label="File from Local Storage" type="file">
        <FileInput
          edited={watchFileInput && "true"}
          text={
            watchFileInput ? watchFileInput[0]?.name : "*.csv, *.xls, *.xlsx"
          }
          accept={".csv, .xls, .xlsx"}
          register={register("file")}
          disabled={isGetting}
        />
      </FormElement>
      <Heading as="h2">Choose one of the options</Heading>
      <FormElement label="Link to Google Sheets">
        <Input
          disabled={isGetting}
          placeholder="https://docs.google.com/spreadsheets/..."
          {...register("link")}
        />
      </FormElement>
      {errors.neitherItem && <Error>{errors?.neitherItem.message}</Error>}
      <Button disabled={isGetting} type="submit">
        {isGetting ? <SpinnerMini /> : "Submit"}
      </Button>
    </Form>
  );
}
