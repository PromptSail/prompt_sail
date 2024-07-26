from organization.models import Organization
from organization.repositories import OrganizationRepository


def get_organization_by_id(
    organization_id: str,
    organization_repository: OrganizationRepository,
) -> Organization:
    """
    Retrieve an organization by its unique identifier.

    :param organization_id: The unique identifier of the organization to be retrieved.
    :param organization_repository: An instance of OrganizationRepository used for accessing project data.
    :return: The Organization object corresponding to the specified identifier.
    """
    organization = organization_repository.find_one({"_id": organization_id})
    return organization


def get_all_organizations_for_owner(organization_repository: OrganizationRepository, owner_id: str) -> list[Organization]:
    """
    Retrieve a list of all organizations.

    :param organization_repository: An instance of OrganizationRepository used for accessing organization data.
    :param owner_id: The unique identifier of the user for whom the organization is to be downloaded..
    :return: A list of all Organization objects stored in the repository.
    """
    organizations = organization_repository.find({"owner": owner_id})
    return organizations


def add_organization(
    organization: Organization,
    organization_repository: OrganizationRepository,
) -> Organization:
    """
    Add a new project to the repository.

    :param organization: The Organization object to be added.
    :param organization_repository: An instance of OrganizationRepository used for storing organization data.
    :return: The newly added Organization object.
    """
    organization_repository.add(organization)
    return organization


def update_organization(
    organization_repository: OrganizationRepository, organization_id: str, fields_to_update: dict
) -> Organization:
    """
    Update an organization with specified fields.

    :param organization_repository: An instance of OrganizationRepository used for organization project data.
    :param organization_id: The unique identifier of the organization to be updated.
    :param fields_to_update: A dictionary containing the fields and values to update in the organization.
    :return: The updated Organization object.
    """
    organization = organization_repository.get(organization_id)
    organization.__dict__.update(**fields_to_update)
    organization_repository.update(organization)
    return organization


def delete_organization(
    organization_id: str,
    organization_repository: OrganizationRepository,
) -> None:
    """
    Delete an organization and associated data.

    :param organization_id: The unique identifier of the organization to be deleted.
    :param organization_repository: An instance of OrganizationRepository used for accessing organization data.
    :return: None
    """
    organization_repository.delete(organization_id)
