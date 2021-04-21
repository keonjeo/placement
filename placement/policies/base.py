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

from oslo_log import versionutils
from oslo_policy import policy

RULE_ADMIN_API = 'rule:admin_api'

DEPRECATED_ADMIN_POLICY = policy.DeprecatedRule(
    name=RULE_ADMIN_API,
    check_str='role:admin'
)

# NOTE(lbragstad): We might consider converting these generic checks into
# RuleDefaults or DocumentedRuleDefaults, but we need to thoroughly vet the
# approach in oslo.policy and consume a new version. Until we have that done,
# let's continue using generic check strings.
SYSTEM_ADMIN = 'rule:system_admin_api'
SYSTEM_READER = 'rule:system_reader_api'
PROJECT_READER = 'rule:project_reader_api'
PROJECT_READER_OR_SYSTEM_READER = 'rule:system_or_project_reader'

_DEPRECATED_REASON = """
Placement API policies are introducing new default roles with scope_type
capabilities. Old policies are deprecated and silently going to be ignored
in the placement 6.0.0 (Xena) release.
"""

rules = [
    policy.RuleDefault(
        "admin_api",
        "role:admin",
        description="Default rule for most placement APIs.",
        scope_types=['system'],
        deprecated_for_removal=True,
        deprecated_reason=_DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.WALLABY,
    ),
    policy.RuleDefault(
        name="system_admin_api",
        check_str='role:admin and system_scope:all',
        description="Default rule for System Admin APIs.",
        deprecated_rule=DEPRECATED_ADMIN_POLICY,
        deprecated_reason=_DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.WALLABY,
    ),
    policy.RuleDefault(
        name="system_reader_api",
        check_str="role:reader and system_scope:all",
        description="Default rule for System level read only APIs.",
        deprecated_rule=DEPRECATED_ADMIN_POLICY,
        deprecated_reason=_DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.WALLABY,
    ),
    policy.RuleDefault(
        name="project_reader_api",
        check_str="role:reader and project_id:%(project_id)s",
        description="Default rule for Project level read only APIs.",
        deprecated_rule=DEPRECATED_ADMIN_POLICY,
        deprecated_reason=_DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.WALLABY,
    ),
    policy.RuleDefault(
        name="system_or_project_reader",
        check_str="rule:system_reader_api or rule:project_reader_api",
        description="Default rule for System+Project read only APIs.",
        deprecated_rule=DEPRECATED_ADMIN_POLICY,
        deprecated_reason=_DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.WALLABY,
    ),
]


def list_rules():
    return rules
