#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Placement API schemas for setting and deleting allocations."""

import copy

from placement.schemas import common


ALLOCATION_SCHEMA = {
    "type": "object",
    "properties": {
        "allocations": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "resource_provider": {
                        "type": "object",
                        "properties": {
                            "uuid": {
                                "type": "string",
                                "format": "uuid"
                            }
                        },
                        "additionalProperties": False,
                        "required": ["uuid"]
                    },
                    "resources": {
                        "type": "object",
                        "minProperties": 1,
                        "patternProperties": {
                            common.RC_PATTERN: {
                                "type": "integer",
                                "minimum": 1,
                            }
                        },
                        "additionalProperties": False
                    }
                },
                "required": [
                    "resource_provider",
                    "resources"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": ["allocations"],
    "additionalProperties": False
}

ALLOCATION_SCHEMA_V1_8 = copy.deepcopy(ALLOCATION_SCHEMA)
ALLOCATION_SCHEMA_V1_8['properties']['project_id'] = {'type': 'string',
                                                      'minLength': 1,
                                                      'maxLength': 255}
ALLOCATION_SCHEMA_V1_8['properties']['user_id'] = {'type': 'string',
                                                   'minLength': 1,
                                                   'maxLength': 255}
ALLOCATION_SCHEMA_V1_8['required'].extend(['project_id', 'user_id'])

# Update the allocation schema to achieve symmetry with the representation
# used when GET /allocations/{consumer_uuid} is called.
# NOTE(cdent): Explicit duplication here for sake of comprehensibility.
ALLOCATION_SCHEMA_V1_12 = {
    "type": "object",
    "properties": {
        "allocations": {
            "type": "object",
            "minProperties": 1,
            # resource provider uuid
            "patternProperties": {
                common.UUID_PATTERN: {
                    "type": "object",
                    "properties": {
                        # generation is optional
                        "generation": {
                            "type": "integer",
                        },
                        "resources": {
                            "type": "object",
                            "minProperties": 1,
                            # resource class
                            "patternProperties": {
                                common.RC_PATTERN: {
                                    "type": "integer",
                                    "minimum": 1,
                                }
                            },
                            "additionalProperties": False
                        }
                    },
                    "required": ["resources"],
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        },
        "project_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "user_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        }
    },
    "additionalProperties": False,
    "required": [
        "allocations",
        "project_id",
        "user_id"
    ]
}


# POST to /allocations, added in microversion 1.13, uses the
# POST_ALLOCATIONS_V1_13 schema to allow multiple allocations
# from multiple consumers in one request. It is a dict, keyed by
# consumer uuid, using the form of PUT allocations from microversion
# 1.12. In POST the allocations can be empty, so DELETABLE_ALLOCATIONS
# modifies ALLOCATION_SCHEMA_V1_12 accordingly.
DELETABLE_ALLOCATIONS = copy.deepcopy(ALLOCATION_SCHEMA_V1_12)
DELETABLE_ALLOCATIONS['properties']['allocations']['minProperties'] = 0
POST_ALLOCATIONS_V1_13 = {
    "type": "object",
    "minProperties": 1,
    "additionalProperties": False,
    "patternProperties": {
        common.UUID_PATTERN: DELETABLE_ALLOCATIONS
    }
}

# A required consumer generation was added to the top-level dict in this
# version of PUT /allocations/{consumer_uuid}. In addition, the PUT
# /allocations/{consumer_uuid}/now allows for empty allocations (indicating the
# allocations are being removed)
ALLOCATION_SCHEMA_V1_28 = copy.deepcopy(DELETABLE_ALLOCATIONS)
ALLOCATION_SCHEMA_V1_28['properties']['consumer_generation'] = {
    "type": ["integer", "null"],
    "additionalProperties": False
}
ALLOCATION_SCHEMA_V1_28['required'].append("consumer_generation")

# A required consumer generation was added to the allocations dicts in this
# version of POST /allocations
REQUIRED_GENERATION_ALLOCS_POST = copy.deepcopy(DELETABLE_ALLOCATIONS)
alloc_props = REQUIRED_GENERATION_ALLOCS_POST['properties']
alloc_props['consumer_generation'] = {
    "type": ["integer", "null"],
    "additionalProperties": False
}
REQUIRED_GENERATION_ALLOCS_POST['required'].append("consumer_generation")
POST_ALLOCATIONS_V1_28 = copy.deepcopy(POST_ALLOCATIONS_V1_13)
POST_ALLOCATIONS_V1_28["patternProperties"] = {
    common.UUID_PATTERN: REQUIRED_GENERATION_ALLOCS_POST
}

# Microversion 1.34 allows an optional mappings object which associates
# request group suffixes with lists of resource provider uuids.
mappings_schema = {
    "type": "object",
    "minProperites": 1,
    "patternProperties": {
        common.GROUP_PAT_1_33: {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string",
                "format": "uuid"
            }
        }
    }
}
ALLOCATION_SCHEMA_V1_34 = copy.deepcopy(ALLOCATION_SCHEMA_V1_28)
ALLOCATION_SCHEMA_V1_34['properties']['mappings'] = mappings_schema
POST_ALLOCATIONS_V1_34 = copy.deepcopy(POST_ALLOCATIONS_V1_28)
POST_ALLOCATIONS_V1_34["patternProperties"] = {
    common.UUID_PATTERN: ALLOCATION_SCHEMA_V1_34
}

# A required consumer type was added to the allocations dicts in this
# version of PUT /allocations/{consumer_uuid} and POST /allocations.
ALLOCATION_SCHEMA_V1_38 = copy.deepcopy(ALLOCATION_SCHEMA_V1_34)
ALLOCATION_SCHEMA_V1_38['properties']['consumer_type'] = {
    "type": "string",
    "pattern": common.CONSUMER_TYPE_PATTERN,
    "minLength": 1,
    "maxLength": 255,
}
ALLOCATION_SCHEMA_V1_38['required'].append("consumer_type")
POST_ALLOCATIONS_V1_38 = copy.deepcopy(POST_ALLOCATIONS_V1_34)
POST_ALLOCATIONS_V1_38["patternProperties"] = {
    common.UUID_PATTERN: ALLOCATION_SCHEMA_V1_38
}
