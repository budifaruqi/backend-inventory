from datetime import datetime
from pydantic import Field
from models.shared.modelDataType import BaseModel, ObjectId
from models.shared.modelSample import SampleModel

class UpdatedData(BaseModel):
    updatedTime: datetime | None = Field(
        default=None,
        title="Updated Time",
        description="Tanggal diubah",
        examples=[SampleModel.datetime_now_utc_2]
    )
    updatedBy: ObjectId | None = Field(
        default=None,
        title="Updated By",
        description="Akun yang melakukan perubahan data",
        examples=[SampleModel.objectId_str_A]
    )

class CreatedData(BaseModel):
    createdTime: datetime | None = Field(
        default=None,
        title="Created Time",
        description="Tanggal dibuat",
        examples=[SampleModel.datetime_now_utc]
    )
    createdBy: ObjectId | None = Field(
        default=None,
        title="Created By",
        description="Akun yang melakukan pembuatan/penambahan data",
        examples=[SampleModel.objectId_str_B]
    )

class DeletedData(BaseModel):
    isDeleted: bool = Field(
        default=False,
        title="Is Deleted",
        description="Data telah dihapus (flaging)",
        examples=[False]
    )

class AuditData(DeletedData, UpdatedData, CreatedData):
    pass