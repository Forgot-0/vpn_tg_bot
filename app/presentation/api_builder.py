# from typing import Any

# from pydantic import ConfigDict, create_model

# from app.domain.exception.base import DomainException
# from app.presentation.schemas.errors import ErrorDetail


# def create_response(
#     excs: DomainException | list[DomainException],
#     description: str = "",
# ) -> dict[str, Any]:

#     if isinstance(excs, DomainException):
#         exc_list: list[DomainException] = [excs]
#     else:
#         exc_list = list(excs)

#     models: list[type[ErrorDetail]] = []
#     examples: dict[str, dict[str, Any]] = {}
#     for exc in exc_list:

#         model_name = f"ErrorResponse_{exc.__class__.__name__}"

#         example_payload: dict[str, Any] = {
#             "code": exc.code,
#             "message": exc.message,
#             "detail": exc.detail,
#         }

#         error_model = create_model(
#             model_name, __base__=ErrorDetail,
#             __config__=ConfigDict(json_schema_extra={"example": example_payload})
#         )

#         models.append(error_model)
#         examples[exc.__class__.__name__] = {
#             "summary": exc.__class__.__name__,
#             "value": {
#                 "error": example_payload,
#                 "status": exc.status,
#                 "request_id": uuid4().hex,
#                 "timestamp": now_utc().timestamp(),
#             },
#         }

#     if len(models) == 1:
#         param_model = ErrorResponse[next(iter(models))]
#         param_model.model_config = ConfigDict(
#             json_schema_extra={"schema_extra": {"example": next(iter(examples.values()))["value"]}}
#         )

#         content = {
#             "application/json": {
#                 "example": next(iter(examples.values()))["value"],
#             }
#         }
#     else:
#         union_type = Union[*models]
#         param_model = ErrorResponse[union_type]
#         first_example = next(iter(examples.values()))["value"]
#         param_model.model_config = ConfigDict(
#             json_schema_extra={
#                 "schema_extra": {
#                     "example": first_example, "examples": {k: v["value"] for k, v in examples.items()}
#                 }
#             },
#         )
#         content = {
#             "application/json": {
#                 "examples": examples,
#             }
#         }

#     return {
#         "description": description,
#         "model": param_model,
#         "content": content,
#     }



# def custom_openapi(app: FastAPI) -> dict[str, Any]:
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title=app.title,
#         version=app.version,
#         description=app.description,
#         routes=app.routes,
#     )

#     response_def = create_response(ValidationException(), description="Validation error")

#     components = openapi_schema.setdefault("components", {})
#     responses = components.setdefault("responses", {})

#     responses["HTTPValidationError"] = {
#         "description": response_def.get("description", "Validation Error"),
#         "content": response_def.get("content", {"application/json": {"example": {}}}),
#     }

#     model = response_def.get("model")
#     if model is not None:

#         model_schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
#         components_schemas = components.setdefault("schemas", {})
#         model_name = getattr(model, "__name__", None) or model.__class__.__name__
#         if isinstance(model_schema, dict):
#             defs = (
#                 model_schema.get("$defs") or
#                 model_schema.get("definitions") or model_schema.get("components", {}).get("schemas")
#             )
#             if defs and isinstance(defs, dict):
#                 for k, v in defs.items():
#                     components_schemas.setdefault(k, v)
#             if "$ref" not in model_schema:
#                 components_schemas.setdefault(model_name, model_schema)
#                 schema_ref = {"$ref": f"#/components/schemas/{model_name}"}
#             else:
#                 schema_ref = model_schema
#             content = responses["HTTPValidationError"].setdefault("content", {})
#             app_json = content.setdefault("application/json", {})
#             app_json["schema"] = schema_ref

#     for path, path_item in openapi_schema.get("paths", {}).items():
#         for method, operation in path_item.items():
#             if not isinstance(operation, dict):
#                 continue
#             responses_obj = operation.get("responses", {})
#             if "422" in responses_obj:
#                 responses_obj["422"] = {"$ref": "#/components/responses/HTTPValidationError"}

#     app.openapi_schema = openapi_schema
#     return app.openapi_schema