# Copyright 2018 Google Inc.  All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Function for parsing genomic region."""

from __future__ import absolute_import

import re
import sys
from typing import Tuple  # pylint: disable=unused-import

# Matches to regions formatted as 'chr12:10,000-20,000'.
_REGION_LITERAL_REGEXP = re.compile(r'^(\S+):([0-9,]+)-([0-9,]+)$')
_DEFAULT_START_POSITION = 0
_DEFAULT_END_POSITION = sys.maxsize


def parse_genomic_region(genomic_region):
  # type: (str) -> Tuple[str, int, int]
  """Parses genomic region that formatted as 'CHROM:START-END'.

  If it does not match `_REGION_LITERAL_REGEXP`, it assumes this region includes
  a full chromosome.

  Returns:
    A tuple containing reference name, start position and end position.
  """
  def _parse_position(pos_str):
    # type: (str) -> int
    return int(pos_str.replace(',', ''))

  matched = _REGION_LITERAL_REGEXP.match(genomic_region)
  if matched:
    ref_name, start, end = matched.groups()
    ref_name = ref_name.strip().lower()
    start = _parse_position(start)
    end = _parse_position(end)
    if start < 0:
      raise ValueError(
          'Start position on a region cannot be negative: {}'.format(start))
    if end <= start:
      raise ValueError('End position must be larger than start position: {} '
                       'vs {}'.format(end, start))
  else:
    # This region includes a full chromosome
    ref_name = genomic_region.strip().lower()
    start = 0
    end = _DEFAULT_END_POSITION
  return ref_name, start, end
