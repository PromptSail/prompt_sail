from settings.models import OrganizationSettings
from settings.repositories import SettingsRepository


def add_settings(
    settings: OrganizationSettings, settings_repository: SettingsRepository
) -> OrganizationSettings:
    """
    Add organization settings to the repository.

    :param settings: The OrganizationSettings object to be added.
    :param settings_repository: An instance of SettingsRepository used for storing organization settings.
    :return: The newly added OrganizationSettings object.
    """
    new_settings = settings_repository.add(settings)
    return new_settings


def get_organization_name(settings_repository: SettingsRepository) -> str:
    """
    Retrieve the name of the organization from the settings.

    :param settings_repository: An instance of SettingsRepository used for accessing organization settings.
    :return: The name of the organization.
    """
    settings = settings_repository.get("settings")
    return settings.organization_name
