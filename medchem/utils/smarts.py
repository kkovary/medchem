from multiprocessing.sharedctypes import Value
from typing import Any, Optional
import datamol as dm


class SMARTSUtils:
    """Collections of utils to build complex SMARTS query more efficiently for non experienced user"""

    @classmethod
    def ortho(
        clc,
        smarts_str1: str,
        smarts_str2: str,
        aromatic_only: bool = False,
    ):
        """
        Returns a recursive smarts string connecting the two input smarts in `ortho` of each other.
        Connexion points needs to be through single or double bonds

        Args:
            smarts_str1: first smarts pattern defining the first functional group
            smarts_str2: second smarts pattern defining the second functional group
            aromatic_only: whether the ring needs to be aromatic or not

        Example:
            to build a smarts for a methyl group in ortho to an oxygen (e.g: 'C1CC(C)C(O)CC1')
            >>> SMARTSUtils.ortho('[#6;!R]', '[#8]')

        Returns:
            smarts: smarts pattern connecting the two input smarts in `ortho` of each other
        """
        if aromatic_only:
            return f"[$({smarts_str1})]-,=!:aa-,=!:[$({smarts_str2})]"
        return f"[$({smarts_str1})]-,=!:[r][r]-,=!:[$({smarts_str2})]"

    @classmethod
    def meta(
        clc,
        smarts_str1: str,
        smarts_str2: str,
        aromatic_only: bool = False,
    ):
        """
        Returns a recursive smarts string connecting the two input smarts in `meta` of each other.
        Connexion points needs to be through single or double bonds

        Args:
            smarts_str1: first smarts pattern defining the first functional group
            smarts_str2: second smarts pattern defining the second functional group
            aromatic_only: whether the ring needs to be aromatic or not

        Example:
            to build a smarts for a methyl group in meta to an oxygen (e.g: 'c1c(C)cc(O)cc1')
            >>> SMARTSUtils.meta('[#6;!R]', '[#8]')

        Returns:
            smarts: smarts pattern connecting the two input smarts in `meta` of each other
        """
        if aromatic_only:
            return f"[$({smarts_str1})]-,=!:aaa-,=!:[$({smarts_str2})]"
        return f"[$({smarts_str1})]-,=!:[r][r][r]-,=!:[$({smarts_str2})]"

    @classmethod
    def para(
        clc,
        smarts_str1: str,
        smarts_str2: str,
        aromatic_only: bool = False,
    ):
        """
        Returns a recursive smarts string connecting the two input smarts in `para` of each other.
        Connexion points needs to be through single or double bonds

        Args:
            smarts_str1: first smarts pattern defining the first functional group
            smarts_str2: second smarts pattern defining the second functional group
            aromatic_only: whether the ring needs to be aromatic or not

        Example:
            to build a smarts for a methyl group in para to an oxygen (e.g: 'c1(C)ccc(O)cc1')
            >>> SMARTSUtils.para('[#6;!R]', '[#8]')

        Returns:
            smarts: smarts pattern connecting the two input smarts in `para` of each other
        """
        if aromatic_only:
            return f"[$({smarts_str1})]-,=!:aaaa-,=!:[$({smarts_str2})]"
        return f"[$({smarts_str1})]-,=!:[r][r][r][r]-,=!:[$({smarts_str2})]"

    @classmethod
    def aliphatic_chain(
        clc,
        min_size: int = 6,
        unbranched: bool = False,
        unsaturated_bondtype: Optional[str] = None,
        allow_hetero_atoms: bool = True,
    ):
        """
        Returns a query that can match a long aliphatic chain

        Args:
            min_size: minimum size of the long chain
            unbranched: whether the chain should be unbranched
            unsaturated_bondtype: additional unsaturated bond type to use for the query. By default, Any bond type (~) is used.
                Single bonds ARE always allowed and bondtype cannot be aromatic
            allow_hetero_atoms: whether the chain can contain hetero atoms

        Example:
            to build a query for a long aliphatic chain of a least 5 atoms (e.g: 'CCC(C)CCC')
            >>> SMARTSUtils.aliphatic_chain(min_size=5)

        Returns:
            smarts: smarts pattern matching a long aliphatic chain
        """
        if unsaturated_bondtype in [dm.AROMATIC_BOND, ":"]:
            raise ValueError("Cannot use aromatic bonds for aliphatic chain")

        include_hets = "" if allow_hetero_atoms else "#6;"
        base_query = "[{}AR0]".format(include_hets)
        bond = "~"
        if unbranched:
            base_query = "[{}R0;D2,D1]".format(include_hets)  # allow terminal too
        if unsaturated_bondtype in [dm.SINGLE_BOND, "-"]:
            bond = ""
        elif unsaturated_bondtype in [dm.DOUBLE_BOND, "="]:
            bond = "-,="
        elif unsaturated_bondtype in [dm.TRIPLE_BOND, "#"]:
            bond = "-,#"
        query = bond.join([base_query] * min_size)
        return query

    @classmethod
    def atom_in_env(
        clc, *smarts_strs, include_atoms: bool = False, union: bool = False
    ):
        """
        Returns a recursive/group smarts to find an atom that fits in the environments as defined by all the input smarts

        Args:
            smarts_strs: list of input patterns defining the environment the atom must fit in. The first atom of each pattern
                should be the atom we want to match to, unless include_atoms is set to True, then [*:99] will be added at the start of each pattern
            include_atoms: whether to include an additional first atom that needs to be in the required environment or not
            union: whether to use the union of the environments or the intersection

        Example:
            you can use this function to construct a complex query if you are not sure about how to write the smarts
            for example, to find a carbon atom that is both in a ring or size 6, bonded to an ethoxy and have a Fluorine in meta
            >>> SMARTSUtils.atom_in_env("[#6;r6][OD2][C&D1]", "[c]aa[F]", union=False) # there are alternative way to write this

        Returns:
            smarts: smarts pattern matching the group/environment
        """
        if include_atoms:
            smarts_strs = [f"[*:99]{sm}" for sm in smarts_strs]

        smarts_strs = [f"$({sm})" for sm in smarts_strs]
        if union:
            query = ",".join(smarts_strs)
        else:
            query = ";".join(smarts_strs)
        if query:
            query = f"[{query}]"
        return query

    @classmethod
    def different_fragment(clc, *smarts_strs):
        """
        Returns a new query that match patterns that are in different fragments.

        !!! warning
            This feature is not supported yet by RDKit. See https://github.com/rdkit/rdkit/issues/1261

        Args:
            smarts_strs: list of input patterns defining the fragments

        Example:
            matching two oxygens in a molecule will work with '[#8].[#8]', but if you want the
            oxygens to be in DIFFERENT fragments, then build the query with:
            >>> SMARTSUtils.different_fragment('[#8]', '[#8]')

        Returns:
            smarts: smarts pattern matching patterns that are in different fragments
        """

        query = ".".join(smarts_strs)
        if query:
            query = f"({query})"
        return query

    @classmethod
    def same_fragment(clc, *smarts_strs):
        """
        Returns a new query that match patterns that are in THE SAME fragment (component)

        !!! warning
            This feature is not supported yet by RDKit. See https://github.com/rdkit/rdkit/issues/1261

        Args:
            smarts_strs: list of input patterns defining the fragments

        Example:
            matching two oxygens in a molecule will work with '[#8].[#8]', but if you want the
            oxygens to be in the SAME fragment, then build the query with:
            >>> SMARTSUtils.same_fragment('[#8]', '[#8]')

        Returns:
            smarts: smarts pattern matching patterns that are in the same component
        """
        return ".".join([f"({sm})" for sm in smarts_strs])

    def build_query(clc, smarts_str: str):
        """Build complex smarts query from a string that may contain keywords like  'NOT', 'AND', 'OR'

        Args:
            smarts_str: input query to turn into a valid smarts

        Returns:
            smarts: valid smarts pattern parsed from input query
        """
