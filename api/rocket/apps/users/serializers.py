from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = BaseUserCreateSerializer.Meta.fields + ("chain_object",)
