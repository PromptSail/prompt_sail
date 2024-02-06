from settings.models import OrganizationSettings, User
from settings.repositories import SettingsRepository


def add_settings(settings: OrganizationSettings, settings_repository: SettingsRepository) -> OrganizationSettings:
    new_settings = settings_repository.add(settings)
    return new_settings


def get_organization_name(settings_repository: SettingsRepository) -> str:
    settings = settings_repository.get("settings")
    return settings.organization_name


def get_users_for_organization(
    settings_repository: SettingsRepository
) -> list[User]:
    organization = settings_repository.get("settings")
    return organization.users
